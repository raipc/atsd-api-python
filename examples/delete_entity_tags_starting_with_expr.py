from atsd_client import connect, connect_url
from atsd_client.services import EntityGroupsService, EntitiesService
from atsd_client.utils import print_tags, print_str

'''
Delete entity tags with names starting with the specified prefix from entities that belongs specific entity group.
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Initialize services

# set the name of entity_group and prefix for tag key
entity_group_name = 'docker-images'
tag_expression = 'env.*'

eg_service = EntityGroupsService(connection)
entities_service = EntitiesService(connection)
entities_list = eg_service.get_entities(entity_group_name, tags=tag_expression)
# exclude entities that have no required tags
entities = [entity for entity in entities_list if entity.tags]

print('entity_name,entity_label,tags')
for entity in entities:
    pretty_tags = print_tags(entity.tags)
    for key in entity.tags:
        entity.tags[key] = ''
    print('%s,%s,%s' % (entity.name, print_str(entity.label), pretty_tags))
    # Uncomment next line to delete tags
    # entities_service.update(entity)
