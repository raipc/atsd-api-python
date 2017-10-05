from datetime import timedelta

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)
entities = filter(lambda entity: entity.lastInsertDate is not None, entities_service.list(limit=100))

for entity in entities:
    metrics = entities_service.metrics(entity.name)
    for m in metrics:
        series = metrics_service.series(m.name, entity.name)
        if len(series) > 1:
            # find one day lag
            lower_limit_date = max(s.lastInsertDate for s in series) - timedelta(days=1)
            for s in series:
                if s.lastInsertDate < lower_limit_date:
                    print("metric: '%s' entity: '%s' tags: %s lastInsertDate: %s" % (
                        s.metric, s.entity, s.tags, s.lastInsertDate))
