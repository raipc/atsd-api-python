from datetime import datetime, timedelta

from atsd_client import connect_url
from atsd_client.services import EntitiesService

'''
Locate series that have no data during the actual time interval (grace_interval) for specified entities.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# set grace_interval to one day
grace_interval_minutes = 24 * 60
# query entities with lastInsertDate
minInsertDate = "1970-01-01T00:00:00.000Z"
# calculate the upper boundary for the allowed lastInsertDate values excluding grace_interval
maxInsertDate = datetime.now() - timedelta(seconds=grace_interval_minutes * 60)

entities_service = EntitiesService(connection)
entities = entities_service.list(expression="name like 'nur*'", minInsertDate=minInsertDate,
                                 maxInsertDate=maxInsertDate)

print('entityName,entityLabel')
for entity in entities:
    print('%s,%s' % (entity.name, entity.label if entity.label is not None else ''))
