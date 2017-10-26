from datetime import timedelta

from atsd_client import connect_url
from atsd_client.services import MetricsService, EntitiesService

'''
Locate lagging series among all the series that differ only in tags (have the same metric and entity) during the 
grace interval. 
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# set grace interval in hours
grace_interval_hours = 1

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

# query all entities that have lastInsertDate, i.e. series
entities = entities_service.list(expression="name LIKE '06*'", minInsertDate="1970-01-01T00:00:00.000")

print('metric, entity, tags, lastInsertDate')
for entity in entities:
    # query all metrics for each entity
    metrics = entities_service.metrics(entity.name)
    for m in metrics:
        # query series list for each metric and entity
        series_list = metrics_service.series(m.name, entity.name)
        # for each list with more than 1 series
        if len(series_list) > 1:
            # calculate maximum of all lastInsertDate's in list and subtract 1 hour
            # it will be lower limit date to compare
            lower_limit_date = max(s.lastInsertDate for s in series_list) - timedelta(
                seconds=grace_interval_hours * 3600)
            for s in series_list:
                # check actual data existence
                if s.lastInsertDate < lower_limit_date:
                    print("%s, %s, %s, %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))
