from atsd_client import connect, connect_url
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, SeriesQuery, ValueFilter, VersioningFilter
from atsd_client.services import SeriesService

'''
Delete data for a given series with tags for the specified date interval.
Only a single matching series is retrieved and delete by setting exact_match=True.
'''

# Connect to ATSD server
# connection = connect('/path/to/connection.properties')
connection = connect_url('https://localhost:8443', 'axibase', 'axibase')

# Series filter
metric = 'anna'
entity = 'anna'

# Specify date interval
startDate = "2018-07-16T19:00:00Z"
endDate = "now"

series_service = SeriesService(connection)

# Query the series to be deleted, use exactMatch to exclude not specified tags
sf = SeriesFilter(metric=metric, exact_match=False)
ef = EntityFilter(entity=entity)
df = DateFilter(start_date=startDate, end_date=endDate)
vf = VersioningFilter(versioned=True)
query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, versioning_filter=vf)
series_list = series_service.query(query)

series = series_list[0]

import pandas as pd

print(series_list)