from datetime import datetime

from atsd_client import connect_url
from atsd_client.models import PropertiesQuery, EntityFilter, DateFilter
from atsd_client.services import EntityGroupsService, EntitiesService, PropertiesService
from atsd_client.utils import print_tags, print_str

'''
Load properties for all entities in group and for type, replace all entity tags that start with 'env.'
with property tags for the given type.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# set the name of entity_group and tag expression
entity_group_name = 'docker-containers'
property_type = 'docker.container.config.env'
tag_expression = 'env.*'

eg_service = EntityGroupsService(connection)
properties_service = PropertiesService(connection)
entities_list = eg_service.get_entities(entity_group_name, tags=tag_expression)
# exclude entities that have no required tags
entities = [entity for entity in entities_list if entity.tags]

entities_service = EntitiesService(connection)

# prepare property query
ef = EntityFilter('entity')
df = DateFilter(start_date="1970-01-01T00:00:00Z", end_date=datetime.now())
property_query = PropertiesQuery(entity_filter=ef, date_filter=df, type=property_type)

print('entity_name,entity_label,tags')
for entity in entities:
    tags_keys = list(entity.tags)
    pretty_tags = print_tags(entity.tags)

    # set actual entity and execute property query
    property_query.set_entity_filter(EntityFilter(entity.name))
    property_item, = properties_service.query(property_query)
    property_tags = property_item.tags

    for key in tags_keys:
        entity.tags[key] = ''
        new_key = key[len(tag_expression[:-1]):]
        entity.tags[new_key] = property_tags[new_key]

    print('%s,%s,%s' % (entity.name, print_str(entity.label), pretty_tags))
    # Uncomment next line to delete tags
    # entities_service.update(entity)
