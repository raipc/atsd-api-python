from datetime import timedelta

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate lagging series among all the series that differ only in tags (have the same metric and entity) during the 
grace interval. 
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# set grace interval in hours
grace_interval_hours = 1

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

# query all entities that have last_insert_date, i.e. series
entities = entities_service.list(expression="name LIKE '06*'", min_insert_date="1970-01-01T00:00:00.000Z")

print('metric,entity,tags,last_insert_date')
for entity in entities:
    # query all metrics for each entity
    metrics = entities_service.metrics(entity.name)
    for m in metrics:
        # query series list for each metric and entity
        series_list = metrics_service.series(m.name, entity.name)
        # for each list with more than 1 series
        if len(series_list) > 1:
            # set lower limit to maximum last insert date over series list minus one hour
            lower_limit_date = max(s.last_insert_date for s in series_list) - timedelta(
                seconds=grace_interval_hours * 3600)
            for s in series_list:
                # check actual data existence
                if s.last_insert_date < lower_limit_date:
                    print("%s,%s,%s,%s" % (s.metric, s.entity, s.tags, s.last_insert_date))
