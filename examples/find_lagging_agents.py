from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

agents = ['nurswgvml007', 'nurswgvml010']

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

for agent in agents:
    metrics = entities_service.metrics(agent)
    for metric in metrics:
        series = metrics_service.series(metric, agent)
        for s in series:
            if s.get_elapsed_minutes() > 24 * 60:
                print("metric: '%s' entity: '%s' tags: %s lastInsertDate: %s" % (
                    s.metric, s.entity, s.tags, s.lastInsertDate))
