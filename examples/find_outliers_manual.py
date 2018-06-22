from datetime import datetime

from atsd_client import connect, connect_url
from atsd_client.models import SeriesQuery, SeriesFilter, EntityFilter, DateFilter
from atsd_client.services import MetricsService, SeriesService

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# set minimum window size to make decision
min_window_size = 5
# 10 days interval in milliseconds
interval_ms = 10 * 24 * 60 * 60 * 1000

svc = SeriesService(connection)
metric_service = MetricsService(connection)

# set metric and entity
metric = 'ca.daily.reservoir_storage_af'
entity = 'ca.oro'

print('Metric: %s\nEntity: %s\n' % (metric, entity))

# prepare query to retrieve data
sf = SeriesFilter(metric=metric, exact_match=True)
ef = EntityFilter(entity=entity)
df = DateFilter(start_date="1970-01-01T00:00:00Z", end_date=datetime.now())

query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)
series, = svc.query(query)

# filter data to exclude not a numbers and non-positive values
data = [s for s in series.data if s.v is not None and s.v > 0]

for i, sample in enumerate(data):

    # prepare data for previous 10 days
    previous_window = []
    for s in data[:i]:
        if (sample.t - interval_ms) <= s.t < sample.t:
            previous_window.append(s)

    # calculate max delta between nearest samples during the previous days
    max_delta_before = -1
    for j, s in enumerate(previous_window[:-1]):
        delta = abs(s.v - previous_window[j + 1].v)
        if delta > max_delta_before:
            max_delta_before = delta

    # prepare data for next 10 days
    next_window = []
    for s in data[i:]:
        if (sample.t + interval_ms) >= s.t > sample.t:
            next_window.append(s)

    # calculate max delta between nearest samples during the next days
    max_delta_after = -1
    for j, s in enumerate(next_window[1:], 1):
        delta = abs(s.v - next_window[j - 1].v)
        if delta > max_delta_after:
            max_delta_after = delta

    # check that there is enough data to make decision
    if len(previous_window) < min_window_size or len(next_window) < min_window_size:
        continue

    before_delta = abs(sample.v - previous_window[-1].v)
    after_delta = abs(sample.v - next_window[0].v)

    if before_delta > 5 * max_delta_before and after_delta > 5 * max_delta_after:
        print('%s %s' % (sample.get_date(), sample.v))
        # replace outlier to improve the data
        sample.v = previous_window[-1].v
