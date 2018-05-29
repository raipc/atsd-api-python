from atsd_client import connect, connect_url
from atsd_client.services import MetricsService
from atsd_client.utils import print_tags

'''
Locate high-cardinality series that have tags more than specified cardinality.
'''

# Connect to ATSD server
#connection = atsd_client.connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Initialize services
metrics_service = MetricsService(connection)

# query all metrics that have last_insert_date, i.e. series
metrics = metrics_service.list(min_insert_date="1970-01-01T00:00:00.000Z")

# set cardinality
cardinality = 8
series_count = 0

print('metric,entity,tags,last_insert_date')
for metric in metrics:
    # query series list for each metric
    series_list = metrics_service.series(metric)
    for s in series_list:
        # check tags cardinality for each series in list
        if len(s.tags) > cardinality:
            series_count += 1
            print("%s,%s,%s,%s" % (s.metric, s.entity, print_tags(s.tags), s.last_insert_date))

print("Number of series that have more than %d tags combinations is %d " % (cardinality, series_count))
