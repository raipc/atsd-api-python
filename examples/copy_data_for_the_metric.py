from datetime import datetime
from atsd_client import connect_url
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, SeriesQuery
from atsd_client.services import SeriesService, MetricsService

'''
Copy data from one metric to the new one.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')
svc = SeriesService(connection)
metrics_service = MetricsService(connection)

# specify source and destination metric names
metric_src = 'metric_src'
metric_dst = 'metric_dst'

# copy series with all entities, specific entity name can be set instead
entity = '*'

# query series with required metric and all entities
sf = SeriesFilter(metric=metric_src)
ef = EntityFilter(entity='*')
df = DateFilter(start_date='1970-01-01T00:00:00Z', end_date=datetime.now())
query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)
series = svc.query(query)

# copy metric meta information
metric = metrics_service.get(metric_src)
metric.name = metric_dst
metrics_service.create_or_replace(metric)

for s in series:
    s.metric = metric_dst
    s.aggregate = None
    svc.insert(s)
