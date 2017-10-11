from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate series that have no data during the actual time interval (grace_interval) for specified entities.
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

# set grace_interval to one day
grace_interval_minutes = 24 * 60

entities_service = EntitiesService(connection)
entities = entities_service.list(expression="name like 'nur*'", minInsertDate="1970-01-01T00:00:00.000Z")

print('entity.name, entity.label')
for entity in entities:
    if entity.get_elapsed_minutes() > grace_interval_minutes:
        print('%s, %s' % (entity.name, entity.label if entity.label is not None else ''))