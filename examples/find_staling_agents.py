from datetime import timedelta

from atsd_client import connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate series that have no data during the interval for one day before entity last_insert_date.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# set grace interval in hours
grace_interval_hours = 1

# list of the agents (entities)
agents = ['nurswgvml007', 'nurswgvml010']

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

for agent in agents:
    # query agent meta information
    entity = entities_service.get(agent)
    if entity is None:
        print('Agent %s not found' % agent)
        continue
    date = entity.last_insert_date
    # query all metrics collecting by agent
    metrics = entities_service.metrics(entity, use_entity_insert_time=True)
    for metric in metrics:
        # check actual data existence
        if date - metric.last_insert_date > timedelta(seconds=grace_interval_hours * 3600):
            print("%s, %s" % (metric.name, agent))
