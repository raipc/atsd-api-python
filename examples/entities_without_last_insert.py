from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService
from atsd_client.utils import print_str

'''
Locate a collection of entities that have no last_insert_date.
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Initialize services
entities_service = EntitiesService(connection)
# query entities without last_insert_date
entity_list = entities_service.list(max_insert_date="1970-01-01T00:00:00.000Z")

print('entity_name,entity_label')
for entity in entity_list:
    print('%s,%s' % (entity.name, print_str(entity.label)))

print("\nEntities count without last insert date is %d." % (len(entity_list)))
