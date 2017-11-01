from atsd_client import connect_url
from atsd_client.services import EntitiesService
from atsd_client.utils import print_str

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

entities_service = EntitiesService(connection)
# query all entities created after specified date
entity_list = entities_service.list(expression="createdDate > '2017-10-16T00:00:00Z' AND tags.status != 'deleted'")

print('entity_name,entity_label')
for entity in entity_list:
    print('%s,%s' % (entity.name, print_str(entity.label)))
