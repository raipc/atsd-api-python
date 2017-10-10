from datetime import datetime, timedelta
from prettytable import PrettyTable

from atsd_client import connect, connect_url
from atsd_client.models import SeriesQuery, SeriesFilter, EntityFilter, DateFilter, ControlFilter, to_iso_local
from atsd_client.services import MetricsService, SeriesService

'''
Find series with data older than `now - (metric.retentionDays + grace_interval_days)`.
'''

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
# connection = connect('/home/axibase/connection.properties')

svc = SeriesService(connection)
metric_service = MetricsService(connection)

metric_list = metric_service.list()
series_count = 0
# ATSD expired data removal schedule frequency, default is one day
grace_interval_days = 1

t = PrettyTable(['Metric', 'Entity', 'Tags', 'Retention Days', 'Threshold', 'Presented Sample Date'])
for metric in metric_list:
    if metric.enabled and metric.persistent and metric.retentionDays != 0:
        # calculate datetime before which there should be data
        threshold = datetime.now() - timedelta(days=metric.retentionDays + grace_interval_days)

        # query series with current metric and all entities from the beginning up to threshold
        # enough to get at least one value so limit set to 1
        sf = SeriesFilter(metric=metric.name)
        ef = EntityFilter(entity='*')
        df = DateFilter(startDate="1970-01-01T00:00:00Z", endDate=threshold)
        cf = ControlFilter(limit=1)
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, control_filter=cf)
        series_list = svc.query(query)
        for sl in series_list:
            if len(sl.data) > 0:
                series_count += 1
                t.add_row([sl.metric, sl.entity, sl.tags, metric.retentionDays, threshold, to_iso_local(sl.data[0].t)])
print t
print("\nSeries count with broken retention date is %d." % series_count)
