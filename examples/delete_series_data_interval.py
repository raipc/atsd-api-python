from atsd_client import connect, connect_url
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, SeriesQuery, ValueFilter
from atsd_client.services import SeriesService

'''
Delete data for a given series with tags for the specified date interval.
Only a single matching series is retrieved and delete by setting exact_match=True.
'''

# Connect to ATSD server
# connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Series filter
metric = 'm-to-delete'
entity = 'e-to-delete'
tags = {'tag_key_1': 'tag_value_1', 'tag_key_2': 'tag_value_2'}

# Specify date interval
startDate = "2018-10-01T00:00:00Z"
endDate = "2018-10-02T00:00:00Z"

# Exclude samples with NaN values (NaN represents deleted values)
expr = '!Float.isNaN(value)'

series_service = SeriesService(connection)

# Query the series to be deleted, use exactMatch to exclude not specified tags
sf = SeriesFilter(metric=metric, tags=tags, exact_match=True)
ef = EntityFilter(entity=entity)
df = DateFilter(start_date=startDate, end_date=endDate)
vf = ValueFilter(expr)
query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, value_filter=vf)
series_list = series_service.query(query)

if len(series_list) > 1:
    raise Exception('There are multiple series meet the requirements')

series = series_list[0]

# Check data existence
if len(series.data) == 0:
    print('No data in required interval')
else:
    # Replace value of samples with NaN
    for sample in series.data:
        print("- Deleting %s, %s " % (sample.get_date(), sample.v))
        sample.v = None
    series.aggregate = None
    # Uncomment next line to delete
    # series_service.insert(series)