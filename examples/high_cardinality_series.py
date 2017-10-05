from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

metrics_service = MetricsService(connection)
metric_list = metrics_service.list(expression="name not like '* *'")
metrics_with_last_insert = filter(lambda metric: metric.lastInsertDate is not None, metric_list)

cardinality = 8
series_count = 0

for metric in metrics_with_last_insert:
    series_list = metrics_service.series(metric)
    for s in series_list:
        if len(s.tags) > cardinality:
            series_count += 1
            print("metric: '%s' entity: '%s' tags: %s lastInsertDate: %s"
                  % (s.metric, s.entity, s.tags, s.lastInsertDate))

print("Number of series that have more than %d tags combinations is %d " % (cardinality, series_count))
