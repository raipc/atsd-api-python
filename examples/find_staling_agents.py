from datetime import timedelta

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate series that have no data during the interval for one day before entity lastInsertDate.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')

# set grace interval in hours
grace_interval_hours = 1

# list of the agents (entities)
agents = ['nurswgvml007', 'nurswgvml010']

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

print('metric, agent')
for agent in agents:
    # query agent meta information
    entity = entities_service.get(agent)
    date = entity.lastInsertDate
    # query all metrics collecting by agent
    metrics = entities_service.metrics(entity, useEntityInsertTime=True)
    for metric in metrics:
        # check actual data existence
        if date - metric.lastInsertDate > timedelta(seconds=grace_interval_hours * 3600):
            print("%s, %s" % (metric.name, agent))
