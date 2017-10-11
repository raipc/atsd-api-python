from datetime import timedelta

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate series that have no data during the interval for one day before entity lastInsertDate.
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

# list of the agents (entities)
agents = ['nurswgvml007', 'nurswgvml010']

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

print('metric, agent, tags, lastInsertDate')
for agent in agents:
    # query agent meta information
    entity = entities_service.get(agent)
    date = entity.lastInsertDate
    # query all metrics collecting by agent
    metrics = entities_service.metrics(entity)
    for metric in metrics:
        # query series list for each agent and metric
        series = metrics_service.series(metric, entity)
        for s in series:
            # check actual data existence
            if date - s.lastInsertDate > timedelta(days=1):
                print("%s, %s, %s, %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))
