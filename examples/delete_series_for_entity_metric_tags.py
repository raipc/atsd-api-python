from atsd_client import connect, connect_url
from atsd_client.services import SeriesService
from atsd_client.models import SeriesDeleteQuery

'''
Delete all series for the specified entity, metric and series tags.
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Set query
entity = 'entity'
metric = 'metric'
tags = {'tag_key_1': 'tag_value_1', 'tag_key_2': 'tag_value_2'}

# Initialize services
series_service = SeriesService(connection)

# Query to match series to be deleted, use exact_match to exclude not specified tags.
# exactMatch is set to True by default. Wildcards are not supported.
query = SeriesDeleteQuery(entity=entity, metric=metric, tags=tags, exact_match=True)

# Uncomment next line to delete series
#response = series_service.delete(query)

#print(response)