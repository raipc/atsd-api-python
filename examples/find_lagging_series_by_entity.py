from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate series that have no data during the actual time interval (grace_interval) using specific entity.
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

# set entity and grace_interval to one day
entity = 'nurswgvml007'
grace_interval_minutes = 24 * 60

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

# query all metrics for entity
metrics = entities_service.metrics(entity)

print('metric, entity, tags, lastInsertDate')
for metric in metrics:
    # query all series for each metric and entity
    series = metrics_service.series(metric, entity)
    for s in series:
        # check actual data existence
        if s.get_elapsed_minutes() > grace_interval_minutes:
            print("%s, %s, %s, %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))
