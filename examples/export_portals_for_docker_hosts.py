#!/usr/bin/python3

from atsd_client import connect
from atsd_client.services import PortalsService, EntitiesService

'''
Queries all entities that are docker hosts, i.e. tags['docker-type'] = 'host'. 
For each host, exports a template portal by name: "Docker Host Breakdown".
'''

# Connect to ATSD server
connection = connect('connection.properties')

# Initialize services
entity_service = EntitiesService(connection)
ps = PortalsService(connection)

entity_limit = 10

# Define expression to retrieve docker hosts
entity_expression = "tags.docker-type='host'"

# Retrieve entities
entities = entity_service.list(expression=entity_expression, limit=entity_limit)

for ent in entities:
    ps.get_portal(name="Docker Host Breakdown", entity=ent.name)
