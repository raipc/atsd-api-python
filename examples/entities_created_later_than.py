from datetime import datetime, timedelta
from dateutil.tz import tzlocal

from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService

date_to_compare = datetime.now(tzlocal()) - timedelta(days=30)

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

entities_service = EntitiesService(connection)
e = entities_service.get('check-created-date')
entity_list = entities_service.list()

required_entities = [entity for entity in entity_list if
                     entity.createdDate is not None and entity.createdDate > date_to_compare]

print("Entities created later than %s" % (date_to_compare.isoformat()))
for entity in required_entities:
    print(entity.name)
