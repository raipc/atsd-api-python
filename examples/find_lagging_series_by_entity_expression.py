from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate series that have no data during the actual time interval (lag) using an expression filter for entity.
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

# set lag in minutes to one day
lag_in_minutes = 24 * 60

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

# query entities that have name started with 06
entities = entities_service.list(expression="name LIKE '06*'")

print('metric, entity, tags, lastInsertDate')
for entity in entities:
    # query all metrics for each entity
    metrics = entities_service.metrics(entity)
    for metric in metrics:
        # query all series for each metric and entity
        series = metrics_service.series(metric, entity)
        for s in series:
            # check actual data existence
            if s.get_elapsed_minutes() > lag_in_minutes:
                print("%s, %s, %s, %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))
