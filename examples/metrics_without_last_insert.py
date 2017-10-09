from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

metric_service = MetricsService(connection)
metric_list = metric_service.list(expression="name not like '* *'", maxInsertDate="1970-01-01T00:00:00.000Z")

for metric in metric_list:
    print(metric.name)
print("Metrics count without last insert date is %d." % (len(metric_list)))
