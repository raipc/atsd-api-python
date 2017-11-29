import random
from datetime import timedelta
from functools import partial

from dateutil.parser import parse

from atsd_client import connect_url
from atsd_client.models import Entity, Series, Sample
from atsd_client.services import EntitiesService, SeriesService


def positive_spline(diff_value, start_value, t, l, x):
    return diff_value * (((x - t).total_seconds() / l.total_seconds()) ** 3) + start_value


def positive_inv_spline(diff_value, start_value, t, l, x):
    return diff_value * (1 + (((x - t).total_seconds() / l.total_seconds()) - 1) ** 3) + start_value


def negative_spline(diff_value, end_value, t, l, x):
    return diff_value * ((1 - ((x - t).total_seconds() / l.total_seconds())) ** 3) + end_value


def linear(diff_value, start_value, t, l, x):
    return start_value if diff_value == 0 else diff_value * (x - t).total_seconds() / l.total_seconds() + start_value


def rand_int(n=65535, start=0):
    return int(random.random() * (n - start)) + start


def next_time(time):
    return time + timedelta(seconds=60 + rand_int(4))


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


ASSET_COUNT = 1
SITE_COUNT = 2
BUILDING_PER_SITE_COUNT = 2
BATCH_COUNT = 3

MIN_TIME = parse('2017-11-15T23:02:00Z')
MAX_TIME = parse('2017-11-19T02:02:00Z')

MIN_JACKET_TEMPERATURE = -10
MAX_JACKET_TEMPERATURE = 80
MIN_AGITATOR_SPEED = 0
MAX_AGITATOR_SPEED = 5
MIN_PRODUCT_TEMPERATURE = 15
MAX_PRODUCT_TEMPERATURE = 40

sites = ['svl', 'nur']
buildings = [['A', 'B'], ['C', 'D']]

connection = connect_url('https://atsd_hostname:8443', 'user', 'password')
entities_service = EntitiesService(connection)
svc = SeriesService(connection)

AGITATION_COUNT = rand_int(5, 2)
BATCH_IDLE_DURATION = rand_int(8, 1)
STAGE_1_DURATION = rand_int(8, 4)
STAGE_2_DURATION = rand_int(10, 5)
STAGE_3_DURATION = rand_int(24, 16)
# Fit batches into the specified range or in proportionally
SUIT_BATCHES = True

print('AGITATION_COUNT = %s' % AGITATION_COUNT)
print('BATCH_IDLE = %s' % BATCH_IDLE_DURATION)
print('STAGE_1_DURATION = %s' % STAGE_1_DURATION)
print('STAGE_2_DURATION = %s' % STAGE_2_DURATION)
print('STAGE_3_DURATION = %s' % STAGE_3_DURATION)
print('SUIT_BATCHES = %s' % SUIT_BATCHES)

stage_2_leaps = []
for i in range(AGITATION_COUNT):
    stage_2_leaps.append(['Stage 2: Enable agitator %d' % i, 3 / 4])
    stage_2_leaps.append((['Stage 2: Product temperature extremum %d' % i, 1 / 4]))
    stage_2_leaps.append((['Stage 2: Disable agitator %d' % i, 1]))

procedures = [['Stage 1: Jacket Heating', 1],
              ['Stage 1: Static Drying', 9],
              *stage_2_leaps,
              ['Stage 2: End', 1],
              ['Stage 3: Product Cooled Down', 2],
              ['Stage 3: Product Heating', 2],
              ['Stage 3: Disable agitator 0', 1],
              ['Stage 3: Enable agitator 0', 15],
              ['Stage 3: Agitator maximum', 1 / 2],
              ['Stage 3: Agitator normal', 1 / 4],
              ['Stage 3: Agitator disable', 1 / 8],
              ['Stage 3: Agitator enable', 6],
              ['Stage 3: Jacket Cooled Down', 1],
              ['Stage 3: Jacket Heating', 1],
              ['Stage 3: Product Cooling', 2],
              ['Stage 3: Disable agitator 1', 1],
              ['Stage 3: Disable agitator 2', 5],
              ['Inactive', 1]]

unit_minutes = ((MAX_TIME - MIN_TIME) / (
    STAGE_1_DURATION + STAGE_2_DURATION + STAGE_3_DURATION + BATCH_IDLE_DURATION)).total_seconds() / BATCH_COUNT / 60

first_stage_length = 0
second_stage_length = 0
third_stage_length = 0
for [name, duration] in procedures:
    if name.startswith('Stage 1'):
        first_stage_length = first_stage_length + duration
    elif name.startswith('Stage 2'):
        second_stage_length = second_stage_length + duration
    elif name.startswith('Stage 3'):
        third_stage_length = third_stage_length + duration

for idx, [name, duration] in enumerate(procedures):
    if name == 'Inactive':
        duration = duration * BATCH_IDLE_DURATION
    elif name.startswith('Stage 1'):
        duration = duration * STAGE_1_DURATION / first_stage_length
    elif name.startswith('Stage 2'):
        duration = duration * STAGE_2_DURATION / second_stage_length
    elif name.startswith('Stage 3'):
        duration = duration * STAGE_3_DURATION / third_stage_length
    procedures[idx] = [name, duration * unit_minutes if SUIT_BATCHES else 60]

jacket_temperature_leaps = dict([(x[0], partial(linear, 0, MAX_JACKET_TEMPERATURE)) for x in stage_2_leaps])
agitator_speed_leaps = dict(
    [(x[0], partial(linear, 0, 0)) if idx % 3 == 2 else (x[0], partial(linear, 0, 2)) for idx, x in
     enumerate(stage_2_leaps)])
product_temperature_leaps = {}

middle = 21.8
step = (28.1 - middle) / AGITATION_COUNT
negative_step = 4.4 + step
for idx in range(0, len(stage_2_leaps), 3):
    enable = stage_2_leaps[idx]
    extremum = stage_2_leaps[idx + 1]
    disable = stage_2_leaps[idx + 2]
    if idx == 0:
        product_temperature_leaps[enable[0]] = partial(positive_inv_spline, 2, 26.6)
        product_temperature_leaps[extremum[0]] = partial(positive_spline, -11, 28.6)
        product_temperature_leaps[disable[0]] = partial(positive_spline, 4.2, 17.6)
    elif idx == len(stage_2_leaps):
        product_temperature_leaps[enable[0]] = partial(linear, 3.9, middle)
        product_temperature_leaps[extremum[0]] = partial(positive_spline, -4.7, 24.7)
        product_temperature_leaps[disable[0]] = partial(positive_spline, 6.1, 20.0)
    elif idx > len(stage_2_leaps) / 2:
        multiplier = (idx - len(stage_2_leaps) / 2) / 3
        product_temperature_leaps[enable[0]] = partial(linear, step, middle + step * multiplier)
        product_temperature_leaps[extremum[0]] = partial(positive_spline, -negative_step,
                                                         middle + step * (multiplier + 1))
        product_temperature_leaps[disable[0]] = partial(positive_spline, negative_step - step * multiplier,
                                                        middle + step * (multiplier + 1) - negative_step)
    else:
        product_temperature_leaps[enable[0]] = partial(linear, step, middle)
        product_temperature_leaps[extremum[0]] = partial(positive_spline, -negative_step, 17.4 + negative_step)
        product_temperature_leaps[disable[0]] = partial(positive_spline, 4.4, 17.4)

metrics = [
    ['jacket_temperature', {
        'Stage 1: Jacket Heating': partial(positive_spline, MAX_JACKET_TEMPERATURE, 0),
        'Stage 1: Static Drying': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        **jacket_temperature_leaps,
        'Stage 2: End': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        'Stage 3: Product Cooled Down': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        'Stage 3: Product Heating': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        'Stage 3: Disable agitator 0': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        'Stage 3: Enable agitator 0': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        'Stage 3: Agitator maximum': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        'Stage 3: Agitator normal': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        'Stage 3: Agitator disable': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        'Stage 3: Agitator enable': partial(linear, 0, MAX_JACKET_TEMPERATURE),
        'Stage 3: Jacket Cooled Down': partial(negative_spline, 90, MIN_JACKET_TEMPERATURE),
        'Stage 3: Jacket Heating': partial(positive_inv_spline, 5, MIN_JACKET_TEMPERATURE),
        'Stage 3: Product Cooling': partial(linear, 0, -5),
        'Stage 3: Disable agitator 1': partial(positive_inv_spline, 5, -5),
        'Stage 3: Disable agitator 2': partial(linear, 0, 0),
        'Inactive': partial(linear, 0, 0)
    }],
    ['agitator_speed', {
        'Stage 1: Jacket Heating': partial(linear, 0, MIN_AGITATOR_SPEED),
        'Stage 1: Static Drying': partial(linear, 0, MIN_AGITATOR_SPEED),
        **agitator_speed_leaps,
        'Stage 2: End': partial(linear, 0, 2),
        'Stage 3: Product Cooled Down': partial(linear, 0, 2),
        'Stage 3: Product Heating': partial(linear, 0, 2),
        'Stage 3: Disable agitator 0': partial(linear, 0, MIN_AGITATOR_SPEED),
        'Stage 3: Enable agitator 0': partial(linear, 0, 2),
        'Stage 3: Agitator maximum': partial(linear, 0, MAX_AGITATOR_SPEED),
        'Stage 3: Agitator normal': partial(linear, 0, 2),
        'Stage 3: Agitator disable': partial(linear, 0, MIN_AGITATOR_SPEED),
        'Stage 3: Agitator enable': partial(linear, 0, 2),
        'Stage 3: Jacket Cooled Down': partial(linear, 0, 2),
        'Stage 3: Jacket Heating': partial(linear, 0, 2),
        'Stage 3: Product Cooling': partial(linear, 0, 2),
        'Stage 3: Disable agitator 1': partial(linear, 0, MIN_AGITATOR_SPEED),
        'Stage 3: Disable agitator 2': partial(linear, 0, MIN_AGITATOR_SPEED),
        'Inactive': partial(linear, 0, MIN_AGITATOR_SPEED)
    }],
    ['product_temperature', {
        'Stage 1: Jacket Heating': partial(positive_spline, 2.4, MIN_PRODUCT_TEMPERATURE),
        'Stage 1: Static Drying': partial(positive_inv_spline, 9.2, 17.4),
        **product_temperature_leaps,
        'Stage 2: End': partial(positive_inv_spline, 2, 26.1),
        'Stage 3: Product Cooled Down': partial(negative_spline, 13.1, MIN_PRODUCT_TEMPERATURE),
        'Stage 3: Product Heating': partial(positive_spline, 3.8, MIN_PRODUCT_TEMPERATURE),
        'Stage 3: Disable agitator 0': partial(positive_inv_spline, 7.3, 18.8),
        'Stage 3: Enable agitator 0': partial(positive_inv_spline, 12.5, 26.1),
        'Stage 3: Agitator maximum': partial(positive_inv_spline, 1, 38.6),
        'Stage 3: Agitator normal': partial(positive_inv_spline, 0.4, 39.6),
        'Stage 3: Agitator disable': partial(positive_spline, -1, MAX_PRODUCT_TEMPERATURE),
        'Stage 3: Agitator enable': partial(positive_inv_spline, 0.7, 38.6),
        'Stage 3: Jacket Cooled Down': partial(linear, 0, MAX_PRODUCT_TEMPERATURE),
        'Stage 3: Jacket Heating': partial(linear, -3.3, MAX_PRODUCT_TEMPERATURE),
        'Stage 3: Product Cooling': partial(linear, -6.6, 36.7),
        'Stage 3: Disable agitator 1': partial(linear, -4, 30.1),
        'Stage 3: Disable agitator 2': partial(negative_spline, 3.1, 23),
        'Inactive': partial(linear, -8, 23)
    }]
]

assets = []
for i in range(ASSET_COUNT):
    site = rand_int(SITE_COUNT)
    building = rand_int(BUILDING_PER_SITE_COUNT)
    assets.append({'id': 'exp.asset-%s' % i, 'site': sites[site], 'building': buildings[site][building]})

for asset in assets:
    entity = Entity(asset['id'], tags={'site': asset['site'], 'building': asset['building']})
    entities_service.create_or_replace(entity)

batch_id = 1400
dataCommandSplines = []
series = []

for asset in assets:
    proc = 0
    t = MIN_TIME

    dataSplines = SplineHolder()
    dataCommandSplines.append([asset, dataSplines])

    while t < MAX_TIME:
        procedure_name = ''

        if proc == 0:
            series.append(Series(asset['id'], 'exp.Unit_BatchID', data=[Sample(time=t, x=batch_id, value=None)]))
            batch_id += 1
            procedure_name = 'Stage 1 Static Drying'
        elif procedures[proc][0] == 'Inactive':
            series.append(Series(asset['id'], 'exp.Unit_BatchID', data=[Sample(time=t, x='Inactive', value=None)]))
        elif procedures[proc][0] == 'Stage 2: Enable agitator 0':
            procedure_name = 'Stage 2 Intermittent Agitation'
        elif procedures[proc][0] == 'Stage 3: Product Cooled Down':
            procedure_name = 'Stage 3 Continuous Agitation'

        if procedure_name:
            series.append(
                Series(asset['id'], 'exp.Unit_Procedure', data=[Sample(time=t, x=procedure_name, value=None)]))

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
