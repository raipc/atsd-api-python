import six

from atsd_client import connect_url
from atsd_client.services import EntityGroupsService, EntitiesService
from atsd_client.utils import pretty_print_dict

'''
Delete entity tags with names starting with the specified prefix from entities that belongs specific entity group.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# set the name of entity_group and prefix for tag key
entity_group_name = 'docker-images'
tag_prefix = 'env.'

eg_service = EntityGroupsService(connection)
entities_service = EntitiesService(connection)
entities_list = eg_service.get_entities(entity_group_name, tags='*')

print('entityName,entityLabel,tags')
for entity in entities_list:
    tags_to_delete = {}
    actual_tags = entity.tags
    for key, value in six.iteritems(actual_tags):
        if key.startswith(tag_prefix):
            tags_to_delete[key] = value
            actual_tags[key] = ''
    # check if there are tags to delete for the entity
    if tags_to_delete:
        print('%s,%s,%s' % (entity.name, entity.label if entity.label is not None else '', pretty_print_dict(tags_to_delete)))
        # Uncomment next line to delete tags
        # entities_service.update(entity)
