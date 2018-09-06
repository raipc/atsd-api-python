#!/usr/bin/env python

from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService

'''
Locate entities by name, using an expression filter
Iterate over the collection and delete each entity
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Initialize services
entity_service = EntitiesService(connection)
entity_limit = 1000

# Define expression to delete matching entities
entity_expression = "name LIKE 'net.source*'"

# Retrieve entities for deletion
entities = entity_service.list(expression=entity_expression, limit=entity_limit)

'''
# Example: delete entities without any tags and with insert date of Sep 1, 2018 or earlier.
# entity_expression = "name.length() == 64 && tags.size() == 0"
entity_expression = "tags.size() == 0"
entity_max_insert_date = '2018-09-01T00:00:00Z'
entity_list = entity_service.list(expression=entity_expression, max_insert_date=entity_max_insert_date, limit=entity_limit)
'''

entity_count = len(entities)
print(
"Found entities: " + str(entity_count) + " for expression= " + entity_expression + " with limit= " + str(entity_limit))

for idx, entity in enumerate(entities):
    print("- Deleting " + entity.name + " : " + str(idx + 1) + "/" + str(entity_count))

    # Uncomment next line to delete
    # entity_service.delete(entity)
