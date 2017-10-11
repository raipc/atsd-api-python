from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

'''
Locate series that have no data during the actual time interval (lag) using specific metric.
Connection.properties will be taken from the same folder where script is.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect()
# connection = atsd_client.connect('/home/axibase/connection.properties')

# set metric and lag in minutes to one day
metric = 'nmon.cpu.busy%'
lag_in_minutes = 24 * 60

metrics_service = MetricsService(connection)

# query all series for metric
series = metrics_service.series(metric)

print('metric, entity, tags, lastInsertDate')
for s in series:
    # check actual data existence
    if s.get_elapsed_minutes() > lag_in_minutes:
        print("%s, %s, %s, %s" % (s.metric, s.entity, s.tags, s.lastInsertDate))
