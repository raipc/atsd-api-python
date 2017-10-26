from datetime import datetime, timedelta

from atsd_client import connect_url
from atsd_client.models import SeriesQuery, SeriesFilter, EntityFilter, DateFilter
from atsd_client.services import MetricsService, SeriesService

interval_days = 10
min_window_size = 5

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

svc = SeriesService(connection)
metric_service = MetricsService(connection)

# set metric and entity
metric = 'ca.daily.reservoir_storage_af'
entity = 'ca.nhg'

sf = SeriesFilter(metric=metric, exactMatch=True)
ef = EntityFilter(entity=entity)
df = DateFilter(startDate="1970-01-01T00:00:00Z", endDate=datetime.now())

query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)
series_list = svc.query(query)

data = series_list[0].data

for i, sample in enumerate(data):
    if sample.v is None:
        continue

    # prepare data for previous 10 days
    window = []
    for idx, s in enumerate(data[:i]):
        if s.v is not None and s.v > 0 \
                and (sample.get_date() - timedelta(days=interval_days)) <= s.get_date() < sample.get_date():
            window.append(s)

    if len(window) < min_window_size:
        continue

    # calculate max delta between nearest samples in prepared data
    max_delta = -1
    for j, s in enumerate(window[:-1]):
        delta = abs(s.v - window[j + 1].v)
        if delta > max_delta:
            max_delta = delta

    if abs(sample.v - window[-1].v) > 5 * max_delta:
        print('%s %s' % (sample.get_date(), sample.v))
        sample.v = None
