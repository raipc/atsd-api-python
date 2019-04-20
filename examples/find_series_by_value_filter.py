from atsd_client import connect, connect_url
from atsd_client.models import *
from atsd_client.services import SeriesService

'''
Retrieve series using value filter to discard out of range values.
'''

# Connect to ATSD server
# connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Set query
metric = 'm-1'
entity = 'e-1'

# Specify date interval
startDate = "2018-05-29T00:00:00Z"
endDate = "2018-05-30T00:00:00Z"

# Retrieve series matching value filter expression
expr = 'value > 1 AND value <= 5'

series_service = SeriesService(connection)

sf = SeriesFilter(metric=metric, exact_match=False)
ef = EntityFilter(entity=entity)
df = DateFilter(start_date=startDate, end_date=endDate)
vf = SampleFilter(expr)
query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, sample_filter=vf)
series_list = series_service.query(query)

print(series_list)
