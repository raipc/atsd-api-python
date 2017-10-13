from atsd_client import connect_url
from atsd_client.services import MetricsService

'''
Locate high-cardinality series that have tags more than specified cardinality.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

metrics_service = MetricsService(connection)

# query all metrics that have lastInsertDate, i.e. series
metrics = metrics_service.list(minInsertDate="1970-01-01T00:00:00.000")

# set cardinality
cardinality = 8
series_count = 0

print('metric, entity, tags, lastInsertDate')
for metric in metrics:
    # query series list for each metric
    series_list = metrics_service.series(metric)
    for s in series_list:
        # check tags cardinality for each series in list
        if len(s.tags) > cardinality:
            series_count += 1
            print("%s, %s, %s, %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))

print("Number of series that have more than %d tags combinations is %d " % (cardinality, series_count))
