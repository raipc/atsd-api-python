import random
from datetime import timedelta
from functools import partial

from dateutil.parser import parse

from atsd_client import connect, connect_url
from atsd_client.models import Entity, Series, Sample
from atsd_client.services import EntitiesService, SeriesService


'''
py version of https://github.com/axibase/batch-viewer/blob/master/net-commands.js
'''

ASSET_COUNT = 10
SITE_COUNT = 2
BUILDING_PER_SITE_COUNT = 2

MIN_TIME = parse('2018-05-15T00:00:00Z')
MAX_TIME = parse('2018-05-16T00:00:00Z')

sites = ['svl', 'nur']
buildings = [['A', 'B'], ['C', 'D']]


def positive_spline(r, m, t, l, x):
    return r * (((x - t).total_seconds() / l.total_seconds()) ** 3) + m


def positive_inv_spline(r, m, t, l, x):
    return r * ((((x - t).total_seconds() / l.total_seconds()) - 1) ** 3) + r + m


def negative_spline(r, m, t, l, x):
    return r * ((1 - ((x - t).total_seconds() / l.total_seconds())) ** 3) + m


def linear(r, m, t, l, x):
    return m if r == 0 else (x - t).total_seconds() * r / l.total_seconds() + m


def rand_int(n=65535):
    return int(random.random() * n)


def next_time(procedure, time):
    if procedure:
        minutes = round(procedure[1] * (random.random() * 1.8 + 0.8))
    else:
        minutes = rand_int(10) + 20

    return time + timedelta(seconds=minutes * 60)


class SplineHolder:
    def __init__(self):
        self.splines = []

    def put_spline(self, t0, t1, metric, spline_builder):
        self.splines.append([t0, t1, metric, partial(spline_builder, t0, t1 - t0)])

    def get_spline(self, metric, t):
        for [s, e, m, f] in self.splines:
            if s <= t < e and m == metric:
                return f
        return None


# Connect to ATSD server
#connection = atsd_client.connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Initialize services
entities_service = EntitiesService(connection)
svc = SeriesService(connection)

procedures = [['Heating', 10], ['Mixing', 5], ['Brewing', 40], ['Cooling', 15], ['Inactive', 5]]

metrics = [['axi.temperature', {
    'Heating': partial(positive_spline, 55, 30),
    'Mixing': partial(positive_inv_spline, 5, 85),
    'Brewing': partial(negative_spline, 10, 80),
    'Cooling': partial(negative_spline, 30, 50),
    'Inactive': partial(linear, -20, 50),
}], ['axi.pressure', {
    'Heating': partial(positive_spline, 12, 10),
    'Mixing': partial(linear, 0, 22),
    'Brewing': partial(positive_spline, 3, 22),
    'Cooling': partial(negative_spline, 15, 10),
    'Inactive': partial(linear, 0, 10),
}], ]

assets = []
for i in range(ASSET_COUNT):
    site = rand_int(SITE_COUNT)
    building = rand_int(BUILDING_PER_SITE_COUNT)
    assets.append({'id': 'axi.asset-%s' % i, 'site': sites[site], 'building': buildings[site][building]})

for asset in assets:
    entity = Entity(asset['id'], tags={'site': asset['site'], 'building': asset['building']})
    entities_service.create_or_replace(entity)

batch_id = 1400
dataCommandSplines = []
series = []

for asset in assets:
    proc = 0
    t = next_time(None, MIN_TIME)

    dataSplines = SplineHolder()
    dataCommandSplines.append([asset, dataSplines])

    while t < MAX_TIME:
        iso = t.isoformat()
        if proc == 0:
            series.append(Series(asset['id'], 'axi.Unit_BatchID', data=[Sample(time=iso, x=batch_id, value=None)]))
            batch_id += 1
        elif procedures[proc][0] == 'Inactive':
            series.append(Series(asset['id'], 'axi.Unit_BatchID', data=[Sample(time=iso, x='Inactive', value=None)]))
        series.append(
            Series(asset['id'], 'axi.Unit_Procedure', data=[Sample(time=iso, x=procedures[proc][0], value=None)]))
        next_t = next_time(procedures[proc], t)
        for [metric, splines] in metrics:
            dataSplines.put_spline(t, next_t, metric, splines[procedures[proc][0]])
        proc = (proc + 1) % len(procedures)
        t = next_t

for [asset, splines] in dataCommandSplines:
    t = MIN_TIME + timedelta(seconds=rand_int(4) + 60)

    while t < MAX_TIME:
        iso = t.isoformat()
        for [metric, d] in metrics:
            spline = splines.get_spline(metric, t)
            if spline:
                value = spline(t)
                value *= (1 + .01 * random.random())
                series.append(Series(asset['id'], metric, data=[Sample(time=iso, value=value)]))
        t = t + timedelta(seconds=rand_int(4) + 60)

svc.insert(*series)
