import sys
from datetime import timedelta

from atsd_client import connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Find series with lastInsertDate more than n hours behind the metric's lastInsertDate.
Print entities of that the series.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# specify metric name
metric_name = "ca.reservoir_storage_af"

# set grace interval in hours
grace_interval_hours = 24 * 7

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

# query required metric meta data
metric = metrics_service.get(metric_name)
if metric is None:
    print('No metric with name %s' % metric_name)
    sys.exit()
elif metric.lastInsertDate is None:
    print('No data for metric name %s' % metric_name)
    sys.exit()

# calculate the upper boundary for the allowed lastInsertDate values excluding grace interval
maxInsertDate = metric.lastInsertDate - timedelta(seconds=grace_interval_hours * 3600)

# query series list for the metric
series_list = metrics_service.series(metric, maxInsertDate=maxInsertDate)

# make dictionary from entity and lastInsertDate, store maximum value of lastInsertDate
various_entities = dict()
for series in series_list:
    lastInsertDate = various_entities.get(series.entity)
    if lastInsertDate is None or lastInsertDate < series.lastInsertDate:
        various_entities[series.entity] = series.lastInsertDate

print('entity (label), lastInsertDate')
for entity in various_entities:
    label = entities_service.get(entity).label
    lastInsertDate = various_entities[entity]
    print('%s (%s), %s' % (entity, label if label is not None else '', lastInsertDate))
