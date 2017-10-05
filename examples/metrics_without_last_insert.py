from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

metric_service = MetricsService(connection)
metric_list = metric_service.list(expression="name not like '* *'")

required_metrics = [metric for metric in metric_list if metric.lastInsertDate is None]

print("Metrics count: %d, %d without last insert date." % (len(metric_list), len(required_metrics)))
for metric in required_metrics:
    print(metric.name)
