from atsd_client import connect_url
from atsd_client.models import SeriesDeleteFilter
from atsd_client.services import SeriesService

'''
Delete all series for the specified entity and all metrics with names starting with the specified prefix.
'''

# Connect to an ATSD server
#conn = connect_url('https://atsd_hostname:8443', 'user', 'password')

conn = connect_url('https://localhost:8443', 'axibase', 'axibase')
# set series
'''
entity = 'e-to-delete'
metric = 'm*'
tags = {'tag_key_1': 'tag_value_1', 'tag_key_2': 'tag_value_2'}
'''
entity = 'anna'
metric = '4150'
tags = {'ver': '16.04'}

series_service = SeriesService(conn)

# delete series, exactMatch is set to `true` by default
series = SeriesDeleteFilter(entity=entity, metric=metric, tags=tags)
# response = series_service.delete(series)

#print(series)