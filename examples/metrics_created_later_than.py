from dateutil import parser

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

'''
Locate a collection of metrics that have been created after specific date.
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

# set specific date
specific_date = parser.parse('2017-10-01T00:00:00Z')

metrics_service = MetricsService(connection)
# query all metrics
metric_list = metrics_service.list()

# select entities created after specific_date
required_metrics = [metric for metric in metric_list if
                    metric.createdDate is not None and metric.createdDate > specific_date]

for metric in required_metrics:
    print(metric.name)

print("Metrics created later than %s." % (specific_date.isoformat()))
