from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService

'''
Locate a collection of entities that have no lastInsertDate.
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

entities_service = EntitiesService(connection)
# query entities without lastInsertDate
entity_list = entities_service.list(maxInsertDate="1970-01-01T00:00:00.000Z")

print('entity.name, entity.label')
for entity in entity_list:
    if entity.lastInsertDate is None:
        print('%s, %s' % (entity.name, entity.label if entity.label is not None else ''))

print("\nEntities count without last insert date is %d." % (len(entity_list)))
