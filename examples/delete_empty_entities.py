#!/usr/bin/env python3

from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService

'''
Delete entities a) without any tags, b) with entity name having 64 characters, and c) which inserted data before 2018-Aug-01.
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Initialize services
entity_service = EntitiesService(connection)
entity_expression = "name.length() == 64 && tags.size() == 0"
entity_limit = 1000
entity_max_insert_date = '2018-08-01T00:00:00Z'
entity_list = entity_service.list(expression=entity_expression, max_insert_date=entity_max_insert_date, limit=entity_limit)

entity_count = len(entity_list)
print("Found " + str(entity_count) + " entities. Limit= " + str(entity_limit))

for idx, entity in enumerate(entity_list):
    print("- Found  " + entity.name + " : " + str(idx + 1) + "/" + str(entity_count) + " : inserted= " + str(entity.last_insert_date) + " : created= " + str(entity.created_date))
    # Uncomment next lines to delete and print delete operation status
    #res = entity_service.delete(entity)
    #print("- Delete " + entity.name + " : " + str(idx + 1) + "/" + str(entity_count) + " : " + str(res))