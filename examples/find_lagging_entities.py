from datetime import datetime, timedelta

from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService
from atsd_client.utils import print_str

'''
Locate series that have no data during the actual time interval (grace_interval) for specified entities.
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# set grace_interval to one day
grace_interval_minutes = 24 * 60
# query entities with last_insert_date
min_insert_date = "1970-01-01T00:00:00.000Z"
# calculate the upper boundary for the allowed last_insert_date values excluding grace_interval
max_insert_date = datetime.now() - timedelta(seconds=grace_interval_minutes * 60)

entities_service = EntitiesService(connection)
entities = entities_service.list(expression="name like 'nur*'", min_insert_date=min_insert_date,
                                 max_insert_date=max_insert_date)

print('entity_name,entity_label')
for entity in entities:
    print('%s,%s' % (entity.name, print_str(entity.label)))
