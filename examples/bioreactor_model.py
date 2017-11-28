import random
from datetime import timedelta
from functools import partial

from dateutil.parser import parse

from atsd_client import connect_url
from atsd_client.models import Entity, Series, Sample
from atsd_client.services import EntitiesService, SeriesService

ASSET_COUNT = 10
SITE_COUNT = 2
BUILDING_PER_SITE_COUNT = 2

MIN_TIME = parse('2017-11-15T23:02:00Z')
MAX_TIME = parse('2017-11-17T02:02:00Z')

min_jacket_temperature = -10
max_jacket_temperature = 80
min_agitator_speed = 0
max_agitator_speed = 5
min_product_temperature = 15
max_product_temperature = 40

sites = ['svl', 'nur']
buildings = [['A', 'B'], ['C', 'D']]


def positive_spline(diff_value, start_value, t, l, x):
    return diff_value * (((x - t).total_seconds() / l.total_seconds()) ** 3) + start_value


def positive_inv_spline(diff_value, start_value, t, l, x):
    return diff_value * ((((x - t).total_seconds() / l.total_seconds()) - 1) ** 3) + diff_value + start_value


def negative_spline(diff_value, end_value, t, l, x):
    return diff_value * ((1 - ((x - t).total_seconds() / l.total_seconds())) ** 3) + end_value


def negative_inv_spline(diff_value, end_value, t, l, x):
    return diff_value * ((1 - ((x - t).total_seconds() / l.total_seconds()) - 1) ** 3) + diff_value + end_value


def linear(diff_value, start_value, t, l, x):
    return start_value if diff_value == 0 else (x - t).total_seconds() * diff_value / l.total_seconds() + start_value


def rand_int(n=65535):
    return int(random.random() * n)


def next_time(time):
    return time + timedelta(seconds=rand_int(4) + 60)


def next_time_p(procedure, time):
    return time + timedelta(seconds=procedure[1] * 60)


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


connection = connect_url('https://atsd_hostname:8443', 'user', 'password')
entities_service = EntitiesService(connection)
svc = SeriesService(connection)

procedures = [['Stage 1: Jacket Heating', 1],
              ['Stage 1: Static Drying', 9],

              ['Stage 2: Enable agitator 1', 3 / 4],
              ['Stage 2: Product temperature extremum 1', 1 / 4],
              ['Stage 2: Disable agitator 1', 1],

              ['Stage 2: Enable agitator 2', 3 / 4],
              ['Stage 2: Product temperature extremum 2', 1 / 4],
              ['Stage 2: Disable agitator 2', 1],

              ['Stage 2: Enable agitator 3', 3 / 4],
              ['Stage 2: Product temperature extremum 3', 1 / 4],
              ['Stage 2: Disable agitator 3', 1],

              ['Stage 2: Enable agitator 4', 3 / 4],
              ['Stage 2: Product temperature extremum 4', 1 / 4],
              ['Stage 2: Disable agitator 4', 1],

              ['Stage 2: Enable agitator 5', 3 / 4],
              ['Stage 2: Product temperature extremum 5', 1 / 4],
              ['Stage 2: Disable agitator 5', 1],

              ['Stage 2: End', 1],
              ['Stage 3: Product Cooled Down', 2],
              ['Stage 3: Product Heating', 2],
              ['Stage 3: Disable agitator 6', 1],
              ['Stage 3: Enable agitator 6', 15],
              ['Stage 3: Agitator maximum', 1 / 2],
              ['Stage 3: Agitator normal', 1 / 4],
              ['Stage 3: Agitator disable', 1 / 8],
              ['Stage 3: Agitator enable', 6],
              ['Stage 3: Jacket Cooled Down', 1],
              ['Stage 3: Jacket Heating', 1],
              ['Stage 3: Product Cooling', 2],
              ['Stage 3: Disable agitator 7', 1],
              ['Stage 3: Disable agitator 8', 5]]

total_units = 0
for [name, duration] in procedures:
    total_units = total_units + duration

unit_minutes = ((MAX_TIME - MIN_TIME) / total_units).total_seconds() / 60
print(unit_minutes)

procedures = [[name, duration * unit_minutes] for [name, duration] in procedures]

metrics = [
    ['jacket_temperature', {
        'Stage 1: Jacket Heating': partial(positive_spline, 80, 0),
        'Stage 1: Static Drying': partial(linear, 0, 80),

        'Stage 2: Enable agitator 1': partial(linear, 0, 80),
        'Stage 2: Product temperature extremum 1': partial(linear, 0, 80),
        'Stage 2: Disable agitator 1': partial(linear, 0, 80),

        'Stage 2: Enable agitator 2': partial(linear, 0, 80),
        'Stage 2: Product temperature extremum 2': partial(linear, 0, 80),
        'Stage 2: Disable agitator 2': partial(linear, 0, 80),

        'Stage 2: Enable agitator 3': partial(linear, 0, 80),
        'Stage 2: Product temperature extremum 3': partial(linear, 0, 80),
        'Stage 2: Disable agitator 3': partial(linear, 0, 80),

        'Stage 2: Enable agitator 4': partial(linear, 0, 80),
        'Stage 2: Product temperature extremum 4': partial(linear, 0, 80),
        'Stage 2: Disable agitator 4': partial(linear, 0, 80),

        'Stage 2: Enable agitator 5': partial(linear, 0, 80),
        'Stage 2: Product temperature extremum 5': partial(linear, 0, 80),
        'Stage 2: Disable agitator 5': partial(linear, 0, 80),

        'Stage 2: End': partial(linear, 0, 80),
        'Stage 3: Product Cooled Down': partial(linear, 0, 80),
        'Stage 3: Product Heating': partial(linear, 0, 80),
        'Stage 3: Disable agitator 6': partial(linear, 0, 80),
        'Stage 3: Enable agitator 6': partial(linear, 0, 80),
        'Stage 3: Agitator maximum': partial(linear, 0, 80),
        'Stage 3: Agitator normal': partial(linear, 0, 80),
        'Stage 3: Agitator disable': partial(linear, 0, 80),
        'Stage 3: Agitator enable': partial(linear, 0, 80),
        'Stage 3: Jacket Cooled Down': partial(negative_spline, 90, -10),
        'Stage 3: Jacket Heating': partial(positive_inv_spline, 5, -10),
        'Stage 3: Product Cooling': partial(linear, 0, -5),
        'Stage 3: Disable agitator 7': partial(positive_inv_spline, 5, -5),
        'Stage 3: Disable agitator 8': partial(linear, 0, 0)
    }],
    ['agitator_speed', {
        'Stage 1: Jacket Heating': partial(linear, 0, 0),
        'Stage 1: Static Drying': partial(linear, 0, 0),

        'Stage 2: Enable agitator 1': partial(linear, 0, 2),
        'Stage 2: Product temperature extremum 1': partial(linear, 0, 2),
        'Stage 2: Disable agitator 1': partial(linear, 0, 0),

        'Stage 2: Enable agitator 2': partial(linear, 0, 2),
        'Stage 2: Product temperature extremum 2': partial(linear, 0, 2),
        'Stage 2: Disable agitator 2': partial(linear, 0, 0),

        'Stage 2: Enable agitator 3': partial(linear, 0, 2),
        'Stage 2: Product temperature extremum 3': partial(linear, 0, 2),
        'Stage 2: Disable agitator 3': partial(linear, 0, 0),

        'Stage 2: Enable agitator 4': partial(linear, 0, 2),
        'Stage 2: Product temperature extremum 4': partial(linear, 0, 2),
        'Stage 2: Disable agitator 4': partial(linear, 0, 0),

        'Stage 2: Enable agitator 5': partial(linear, 0, 2),
        'Stage 2: Product temperature extremum 5': partial(linear, 0, 2),
        'Stage 2: Disable agitator 5': partial(linear, 0, 0),

        'Stage 2: End': partial(linear, 0, 2),
        'Stage 3: Product Cooled Down': partial(linear, 0, 2),
        'Stage 3: Product Heating': partial(linear, 0, 2),
        'Stage 3: Disable agitator 6': partial(linear, 0, 0),
        'Stage 3: Enable agitator 6': partial(linear, 0, 2),
        'Stage 3: Agitator maximum': partial(linear, 0, 5),
        'Stage 3: Agitator normal': partial(linear, 0, 2),
        'Stage 3: Agitator disable': partial(linear, 0, 0),
        'Stage 3: Agitator enable': partial(linear, 0, 2),
        'Stage 3: Jacket Cooled Down': partial(linear, 0, 2),
        'Stage 3: Jacket Heating': partial(linear, 0, 2),
        'Stage 3: Product Cooling': partial(linear, 0, 2),
        'Stage 3: Disable agitator 7': partial(linear, 0, 0),
        'Stage 3: Disable agitator 8': partial(linear, 0, 0)
    }],
    ['product_temperature', {
        'Stage 1: Jacket Heating': partial(positive_spline, 2.4, 15),
        'Stage 1: Static Drying': partial(positive_inv_spline, 9.2, 17.4),

        'Stage 2: Enable agitator 1': partial(positive_inv_spline, 2, 26.6),
        'Stage 2: Product temperature extremum 1': partial(negative_inv_spline, 11, 17.6),
        'Stage 2: Disable agitator 1': partial(positive_spline, 4.2, 17.6),

        'Stage 2: Enable agitator 2': partial(linear, 1, 21.8),
        'Stage 2: Product temperature extremum 2': partial(negative_inv_spline, 5.4, 17.4),
        'Stage 2: Disable agitator 2': partial(positive_spline, 4.2, 17.4),

        'Stage 2: Enable agitator 3': partial(linear, 1, 21.6),
        'Stage 2: Product temperature extremum 3': partial(negative_inv_spline, 5, 17.6),
        'Stage 2: Disable agitator 3': partial(positive_spline, 4.2, 17.6),

        'Stage 2: Enable agitator 4': partial(linear, 1, 21.8),
        'Stage 2: Product temperature extremum 4': partial(negative_inv_spline, 5, 17.8),
        'Stage 2: Disable agitator 4': partial(positive_spline, 5.6, 18.1),

        'Stage 2: Enable agitator 5': partial(linear, 1, 23.7),
        'Stage 2: Product temperature extremum 5': partial(negative_inv_spline, 4.7, 20.0),
        'Stage 2: Disable agitator 5': partial(positive_spline, 6.1, 20.0),

        'Stage 2: End': partial(positive_inv_spline, 2, 26.1),
        'Stage 3: Product Cooled Down': partial(negative_spline, 13.1, 15.0),
        'Stage 3: Product Heating': partial(positive_spline, 3.8, 15.0),
        'Stage 3: Disable agitator 6': partial(positive_inv_spline, 7.3, 18.8),
        'Stage 3: Enable agitator 6': partial(positive_inv_spline, 12.5, 26.1),
        'Stage 3: Agitator maximum': partial(positive_inv_spline, 1.3, 38.6),
        'Stage 3: Agitator normal': partial(positive_inv_spline, 1, 39.3),
        'Stage 3: Agitator disable': partial(negative_inv_spline, 1, 39.3),
        'Stage 3: Agitator enable': partial(positive_inv_spline, 0.7, 38.6),
        'Stage 3: Jacket Cooled Down': partial(linear, 0, 40.0),
        'Stage 3: Jacket Heating': partial(negative_spline, 5, 35.0),
        'Stage 3: Product Cooling': partial(negative_spline, 4.2, 30.8),
        'Stage 3: Disable agitator 7': partial(negative_spline, 4.7, 26.1),
        'Stage 3: Disable agitator 8': partial(negative_spline, 7.8, 18.3)
    }]
]

assets = []
for i in range(ASSET_COUNT):
    site = rand_int(SITE_COUNT)
    building = rand_int(BUILDING_PER_SITE_COUNT)
    assets.append({'id': 'axi.asset-%s' % i, 'site': sites[site], 'building': buildings[site][building]})

for asset in assets:
    entity = Entity(asset['id'], tags={'site': asset['site'], 'building': asset['building']})
    entities_service.create_or_replace(entity)

dataCommandSplines = []
series = []

for asset in assets:
    proc = 0
    t = MIN_TIME

    dataSplines = SplineHolder()
    dataCommandSplines.append([asset, dataSplines])

    while t < MAX_TIME:
        next_t = next_time_p(procedures[proc], t)
        for [metric, splines] in metrics:
            dataSplines.put_spline(t, next_t, metric, splines[procedures[proc][0]])
        proc = (proc + 1) % len(procedures)
        t = next_t

for [asset, splines] in dataCommandSplines:
    t = MIN_TIME

    while t < MAX_TIME:
        for [metric, d] in metrics:
            spline = splines.get_spline(metric, t)
            if spline:
                value = spline(t)
                series.append(Series(asset['id'], metric, data=[Sample(time=t, value=value)]))
        t = next_time(t)

svc.insert(*series)
