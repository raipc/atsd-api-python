from dateutil import parser

from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService

'''
Locate a collection of entities that have been created after specific date.
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

# set specific date
specific_date = parser.parse('2017-10-01T00:00:00Z')

entities_service = EntitiesService(connection)
# query all entities
entity_list = entities_service.list()

# select entities created after specific_date
required_entities = [entity for entity in entity_list if
                     entity.createdDate is not None and entity.createdDate > specific_date]

for entity in required_entities:
    print(entity.name)

print("\nEntities created later than %s." % (specific_date.isoformat()))
