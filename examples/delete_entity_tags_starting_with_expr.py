from atsd_client import connect_url
from atsd_client.services import EntityGroupsService, EntitiesService

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

print('entityName,entityLabel')
for entity in entities_list:
    need_update = False
    actual_tags = entity.tags
    for key in actual_tags:
        if key.startswith(tag_prefix):
            actual_tags[key] = ''
            # mark entity to be updated
            need_update = True
    if need_update:
        print('%s,%s' % (entity.name, entity.label if entity.label is not None else ''))
        # Uncomment next line to delete tags
        # entities_service.update(entity)
