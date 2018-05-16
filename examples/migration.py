import ast
import os
from os.path import splitext

from atsd_client import connect_url
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, SeriesQuery, Series, Aggregate, \
    TransformationFilter, TimeUnit, AggregateType, Rate, Group, InterpolateType
from atsd_client.services import SeriesService

'''
The test should compare series query responses for the given metric, entity, tags, and start/end dates before and
after ATSD migration, compare results.

Naming convention: query-${metric}-${entity}-${tags}-${type}.json
Tags must be divide with ';' between pairs and with '=' between tag key and value.
Instead of query can be specified rate or group if required.

query-cpu_busy-nurswgvml007-all-DETAIL.json
query-cpu_busy-nurswgvml007-all-PERCENTILE_90+DELTA.json
query-disk_used-nurswgvml006-all-all.json
query-disk_used-nurswgvml006-all-DETAIL.json
query-disk_used-nurswgvml006-all-MIN+MAX.json
query-disk_used-nurswgvml006-all-MIN.json
query-disk_used-nurswgvml006-all-WTAVG.json
query-log_event_counter-nurswgvml007-command=com.axibase.tsd.Server;level=INFO;logger=com.axibase.tsd.service.config.ServerPropertiesReader-all.json
rate-cpu_busy-nurswgvml007-all-DETAIL.json
group-disk_used-nurswgvml006-all-DETAIL.json
rate+group-collectd.cpu.busy-nurswghbs001-all-MIN.json
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')
svc = SeriesService(connection)

# set start_date and end_date
start_date = '2018-05-07T07:00:00Z'
end_date = '2018-05-08T08:00:00Z'

# list all json files from the current directory
files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.json')]

for filename in files:
    # parse filename to get series information
    query, metric_name, entity_name, tags, aggregate_types = splitext(filename)[0].split('-')

    # prepare tags
    exact_match = tags != 'all'
    if exact_match:
        tags = dict(tag.split('=') for tag in tags.split(';'))
    else:
        tags = None

    # prepare aggregate types
    if aggregate_types == 'all':
        aggregate_types = [key for key in dir(AggregateType) if not key.startswith('_')]
    else:
        aggregate_types = aggregate_types.split('+')

    # try to retrieve series from the previous query
    expected_series = []
    with open(filename) as fp:
        line = fp.readline()
        while line:
            series = Series.from_dict(ast.literal_eval(line))
            expected_series.extend(series)
            line = fp.readline()

    # prepare series query
    sf = SeriesFilter(metric=metric_name, tags=tags, exact_match=exact_match)
    ef = EntityFilter(entity=entity_name)
    df = DateFilter(start_date=start_date, end_date=end_date)
    aggregate = Aggregate(period={'count': 7, 'unit': TimeUnit.MINUTE}, threshold={'min': 10, 'max': 90},
                          types=aggregate_types, order=1)
    tf = TransformationFilter(aggregate=aggregate)

    # add rate and group to the transformation filter if specified instead of query
    if query != 'query':
        for attr in query.split('+'):
            if attr == 'rate':
                tf.set_rate(Rate(period={'count': 3, 'unit': TimeUnit.MINUTE}))
            elif attr == 'group':
                tf.set_group(Group(type=AggregateType.SUM, truncate=True, order=0,
                                   interpolate={'type': InterpolateType.LINEAR, 'extend': True},
                                   period={'count': 4, 'unit': TimeUnit.MINUTE}))

    query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, transformation_filter=tf)
    actual_series = svc.query(query)

    if actual_series != expected_series:
        print(filename)
        with open(filename, 'w') as fp:
            serialized = [series.to_dictionary() for series in actual_series]
            fp.write('%s\n' % serialized)
