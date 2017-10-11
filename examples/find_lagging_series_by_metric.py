from datetime import timedelta, datetime

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

'''
Locate series that have no data during the actual time interval (grace_interval) using specific metric.
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

# set metric and grace_interval to one day
metric = 'nmon.cpu.busy%'
grace_interval_minutes = 24 * 60
# query entities with lastInsertDate
minInsertDate = "1970-01-01T00:00:00.000Z"
# calculate the upper boundary for the allowed lastInsertDate values excluding grace_interval
maxInsertDate = datetime.now() - timedelta(seconds=grace_interval_minutes * 60)
metrics_service = MetricsService(connection)

# query all series for metric
series = metrics_service.series(metric, minInsertDate=minInsertDate, maxInsertDate=maxInsertDate)

print('metric, entity, tags, lastInsertDate')
for s in series:
    print("%s, %s, %s, %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))
