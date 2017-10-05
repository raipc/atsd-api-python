from datetime import datetime, timedelta
from dateutil.tz import tzlocal

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

date_to_compare = datetime.now(tzlocal()) - timedelta(days=30)

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

metrics_service = MetricsService(connection)
metric_list = metrics_service.list(expression="name not like '* *'")

required_metrics = [metric for metric in metric_list if
                    metric.createdDate is not None and metric.createdDate > date_to_compare]
print("Metrics created later than %s" % (date_to_compare.isoformat()))
for metric in required_metrics:
    print(metric.name)
