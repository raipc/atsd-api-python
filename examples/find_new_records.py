from datetime import timedelta, datetime
from dateutil.tz import tzlocal

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

date_to_compare = datetime.now(tzlocal()) - timedelta(days=1)

metrics_service = MetricsService(connection)
metric_list = metrics_service.list(expression="name not like '* *'")
new_metrics = filter(lambda metric: metric.createdDate and metric.createdDate > date_to_compare, metric_list)

entities_service = EntitiesService(connection)
entity_list = entities_service.list()
new_entities = filter(lambda entity: entity.createdDate and entity.createdDate > date_to_compare, entity_list)

print("New metrics and entities created count during the last day (from %s) are %d and %s correspondingly " % (
    date_to_compare.isoformat(), len(new_metrics), len(new_entities)))
for metric in new_metrics:
    print(metric.name)
print('---------')
for entity in new_entities:
    print(entity.name)
