from __future__ import print_function

import os
from os import path


from atsd_client import connect_url
from atsd_client.services import EntitiesService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
entities_service = EntitiesService(connection)
entity_list = entities_service.list()

required_entities = [entity for entity in entity_list if entity.lastInsertDate is None]

with open(os.path.splitext(path.abspath(__file__))[0] + ".txt", 'w') as f:
    print("Entities count: %d, %d without last insert date." % (len(entity_list), len(required_entities)), file=f)
    for entity in required_entities:
        print(entity.name, file=f)
