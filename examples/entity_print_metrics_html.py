from datetime import datetime, timedelta
from prettytable import PrettyTable

from atsd_client import connect, connect_url
from atsd_client.services import MetricsService, EntitiesService

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

entity = 'my-entity'

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

# query all metrics for entity
metrics = entities_service.metrics(entity, tags='frequency,seasonal_adjustment,observation_start,observation_end,category,parent_category', limit=5)
t = PrettyTable(['Top Category', 'Category', 'Name', 'Label', 'Frequency', 'Adjustment', 'Observation Start', 'Observation End'])

# iterate over metrics and add their fields/tags as rows into a PrettyTable
for metric in metrics:
	t.add_row([metric.tags['category'], metric.tags['parent_category'], metric.name, metric.label, metric.tags['frequency'], metric.tags['seasonal_adjustment'], metric.tags['observation_start'], metric.tags['observation_end']])

# Sort metrics by name
t.sortby = "Name"

# Print metrics as ASCII table
#print(t)

# Print metrics as HTML table with header
print(t.get_html_string(title="Available Metrics"))
