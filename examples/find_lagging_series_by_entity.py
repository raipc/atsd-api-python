from datetime import datetime, timedelta

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService
from atsd_client.utils import print_tags

'''
Locate series that have no data during the actual time interval (grace_interval) using specific entity.
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# set entity and grace_interval to one day
entity = 'nurswgvml007'
grace_interval_minutes = 24 * 60
# query entities with last_insert_date
min_insert_date = "1970-01-01T00:00:00.000Z"
# calculate the upper boundary for the allowed last_insert_date values excluding grace_interval
max_insert_date = datetime.now() - timedelta(seconds=grace_interval_minutes * 60)

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

# query all metrics for entity
metrics = entities_service.metrics(entity)

print('metric,entity,tags,last_insert_date')
for metric in metrics:
    # query all series for each metric and entity
    series = metrics_service.series(metric, entity, min_insert_date=min_insert_date, max_insert_date=max_insert_date)
    for s in series:
        print("%s,%s,%s,%s" % (s.metric, s.entity, print_tags(s.tags), s.last_insert_date))
