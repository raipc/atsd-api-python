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
entity_expression = "name LIKE 'net.source*'"
entity_limit = 1000
entities = entity_service.list(expression=entity_expression, limit=entity_limit)

entity_count = len(entities)
print(
"Found entities: " + str(entity_count) + " for expression= " + entity_expression + " with limit= " + str(entity_limit))

for idx, entity in enumerate(entities):
    print("- Deleting " + entity.name + " : " + str(idx + 1) + "/" + str(entity_count))

    # Uncomment next line to delete
    # entity_service.delete(entity)
