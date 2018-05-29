from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService
from atsd_client.utils import print_str

'''
Delete specific entity tags by name from entities that match an expression.
'''

# Connect to ATSD server
#connection = atsd_client.connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Initialize services
entities_service = EntitiesService(connection)

# set an expression to query entities with non-empty 'category' and 'subcategory' tags
expression = "tags.category != '' AND tags.subcategory != ''"
# list the tags to be deleted
tags_to_delete = ['original_price', 'last_price', 'last_average_price', 'last_amount']

entities_list = entities_service.list(expression=expression, tags=tags_to_delete)

print('entity_name,entity_label')
for entity in entities_list:
    need_update = False
    actual_tags = entity.tags
    for key in tags_to_delete:
        if key in actual_tags:
            actual_tags[key] = ''
            # mark entity to be updated
            need_update = True
    if need_update:
        print('%s,%s' % (entity.name, print_str(entity.label)))
        # Uncomment next line to delete tags
        # entities_service.update(entity)
