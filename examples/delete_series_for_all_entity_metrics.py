from atsd_client import connect_url
from atsd_client.services import EntitiesService, SeriesService
from atsd_client.models import SeriesDeleteQuery

'''
Delete series for all metrics for the specified entity with names starting with the specified prefix.
'''

# Connect to an ATSD server
conn = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Set query
entity = "entity"
metric_expr = "name LIKE 'me*'"

entities_service = EntitiesService(conn)
series_service = SeriesService(conn)

# Query all metrics for entity
metrics = entities_service.metrics(entity=entity, expression=metric_expr)

if not metrics:
    print("No metrics are found for entity " + entity)
else:
    # Delete series for each metric
    for metric in metrics:
        query = SeriesDeleteQuery(entity=entity, metric=metric.name, exact_match=False)
        print("deleting ", entity, metric.name)
        # Uncomment next line to delete series
        #response = series_service.delete(query)
        #print(response)
