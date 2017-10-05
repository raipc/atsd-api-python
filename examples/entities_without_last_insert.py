from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

entities_service = EntitiesService(connection)
entity_list = entities_service.list()

required_entities = [entity for entity in entity_list if entity.lastInsertDate is None]

print("Entities count: %d, %d without last insert date." % (len(entity_list), len(required_entities)))
for entity in required_entities:
    print(entity.name)
