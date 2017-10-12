from datetime import datetime, timedelta

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate series that have no data during the actual time interval (grace_interval) using specific entity.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')

# set entity and grace_interval to one day
entity = 'nurswgvml007'
grace_interval_minutes = 24 * 60
# query entities with lastInsertDate
minInsertDate = "1970-01-01T00:00:00.000Z"
# calculate the upper boundary for the allowed lastInsertDate values excluding grace_interval
maxInsertDate = datetime.now() - timedelta(seconds=grace_interval_minutes * 60)

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

# query all metrics for entity
metrics = entities_service.metrics(entity)

print('metric, entity, tags, lastInsertDate')
for metric in metrics:
    # query all series for each metric and entity
    series = metrics_service.series(metric, entity, minInsertDate=minInsertDate, maxInsertDate=maxInsertDate)
    for s in series:
        print("%s, %s, %s, %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))
