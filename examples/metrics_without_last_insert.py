from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

'''
Locate a collection of metrics that have no last_insert_date.
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Initialize services
metric_service = MetricsService(connection)
# query entities without last_insert_date
metric_list = metric_service.list(max_insert_date="1970-01-01T00:00:00.000Z")
metrics_count = 0

print('metric_name')
for metric in metric_list:
    if metric.enabled and metric.persistent \
            and metric.retention_days == 0 and metric.series_retention_days == 0:
        metrics_count += 1
        print(metric.name)

print("\nMetrics count without last insert date is %d." % metrics_count)
