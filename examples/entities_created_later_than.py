from dateutil import parser

from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')

entities_service = EntitiesService(connection)
# query all entities created after specified date
entity_list = entities_service.list(expression="createdDate > '2017-10-01T00:00:00Z'")

print('entity.name, entity.label')
for entity in entity_list:
    print('%s, %s' % (entity.name, entity.label if entity.label is not None else ''))
