import sys
from datetime import timedelta

from atsd_client import connect_url
from atsd_client.services import MetricsService

'''
Find entities of series more than n hours behind the metric's lastInsertDate.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# specify metric name
metric_name = "ca.reservoir_storage_af"

# set grace interval in hours
grace_interval_hours = 24 * 7

metrics_service = MetricsService(connection)

# query required metric meta data
metric = metrics_service.get(metric_name)
if metric is None:
    print('No metric with name %s' % metric_name)
    sys.exit()

# calculate the upper boundary for the allowed lastInsertDate values excluding grace interval
maxInsertDate = metric.lastInsertDate - timedelta(seconds=grace_interval_hours * 3600)

# query series list for the metric
series_list = metrics_service.series(metric, maxInsertDate=maxInsertDate)

for series in series_list:
    print(series.entity)
