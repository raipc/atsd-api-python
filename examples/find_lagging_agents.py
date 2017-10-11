from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate series that have no data during the actual time interval (lag) for specific entities (agents).
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

# list of the agents (entities)
agents = ['nurswgvml007', 'nurswgvml010']
# set lag in minutes to one day
lag_in_minutes = 24 * 60

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

print('metric, agent, tags, lastInsertDate')
for agent in agents:
    # query all metrics for agents
    metrics = entities_service.metrics(agent)
    for metric in metrics:
        # query all series for each metric and agent
        series = metrics_service.series(metric, agent)
        for s in series:
            # check actual data existence
            if s.get_elapsed_minutes() > lag_in_minutes:
                print("%s, %s, %s, %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))