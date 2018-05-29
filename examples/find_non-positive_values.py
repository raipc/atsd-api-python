from datetime import datetime

from atsd_client import connect, connect_url
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, SeriesQuery
from atsd_client.services import SeriesService, MetricsService

'''
Load all series values that are non-positive for the specified metric.
Optionally, if deleteValues parameter is set replace these values with NaN.
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# disable deleting inappropriate values
deleteValues = False

# specify metric name
metric_name = "ca.daily.reservoir_storage_af"

svc = SeriesService(connection)
metrics_service = MetricsService(connection)

# query series with current metric and all entities
sf = SeriesFilter(metric=metric_name)
ef = EntityFilter(entity='*')
df = DateFilter(start_date="1970-01-01T00:00:00Z", end_date=datetime.now())
query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)
series = svc.query(query)

if deleteValues:
    print('Inappropriate values will be deleted.\n')
else:
    print('Leave as is inappropriate values.\n')

print('metric,entity,tags,data')
for s in series:
    # filter non-positive values
    s.data = [sample for sample in s.data if sample.v is not None and sample.v <= 0]

    if len(s.data) > 0:
        print("%s,%s,%s,%s" % (s.metric, s.entity, s.tags, [sample.v for sample in s.data]))
        if deleteValues:
            # delete replace inappropriate values with Nan
            for sample in s.data:
                print("- Deleting %s, %s " % (sample.get_date(), sample.v))
                sample.v = None
            s.aggregate = None
            # Uncomment next line to delete
            # svc.insert(s)
