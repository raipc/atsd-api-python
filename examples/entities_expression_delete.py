#!/usr/bin/env python
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

from atsd_client import connect_url
from atsd_client.services import EntitiesService
from atsd_client.models import Entity

'''
Locate entities by name, using an expression filter
Iterate over the collection and delete each entity
'''

conn = connect_url('http://atsd_hostname:8088', 'user', 'pwd')
#conn = atsd_client.connect('/home/axibase/connection.properties')

entity_service = EntitiesService(conn)
entity_expression = "name LIKE 'net.source*'"
entity_limit = 1000
entities = entity_service.list(expression=entity_expression, limit=entity_limit)

entity_count = len(entities)
print("Found entities: " + str(entity_count) + " for expression= " + entity_expression + " with limit= " + str(entity_limit))

for idx, entity in enumerate(entities):

    print("- Deleting " + entity.name +  " : " + str(idx+1) + "/" + str(entity_count))

    # Uncomment next line to delete
    entity_service.delete(entity)