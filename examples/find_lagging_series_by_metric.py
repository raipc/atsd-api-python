from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

metrics_service = MetricsService(connection)

metric = ' nmon.cpu.busy%'
series = metrics_service.series(metric)

for s in series:
    if s.get_elapsed_minutes() > 24 * 60:
        print("metric: '%s' entity: '%s' tags: %s lastInsertDate: %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))
