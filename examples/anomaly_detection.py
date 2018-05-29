#!/usr/bin/python3

import argparse
from datetime import timedelta, datetime

import time
from luminol.anomaly_detector import AnomalyDetector

from atsd_client import connect, connect_url
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, SeriesQuery, TransformationFilter, TimeUnit, \
    Message, Aggregate, AggregateType, Interpolate, InterpolateFunction
from atsd_client.services import EntitiesService, MetricsService, SeriesService, MessageService
from atsd_client.utils import print_tags

'''
Find anomaly values through the all series that have at least one value 
during the last hours with minimal score for a given entity. 
'''


def log(logging_message):
    if args.verbose == 1:
        print(logging_message)


def format_t(timestamp):
    return time.strftime(time_format, time.localtime(timestamp))


parser = argparse.ArgumentParser(description='Anomaly detection using luminol package.')
parser.add_argument('--last_hours', '-lh', type=float, help='interested number of hours', default=24)
parser.add_argument('--min_score', '-ms', type=float, help='score threshold', default=0)
parser.add_argument('--entity', '-e', type=str, help='entity to monitor', default='060190011')
parser.add_argument('--metric_filter', '-mf', type=str, help='filter for metric names')
parser.add_argument('--aggregate_period', '-ap', type=int, help='aggregate period', default=0)
parser.add_argument('--interpolate_period', '-ip', type=int, help='interpolate period', default=60)
parser.add_argument('--data_interval', '-di', type=int, help='requested data to analyze', default=24)
parser.add_argument('--verbose', '-v', action="count", help="enable series processing logging")
args = parser.parse_args()

time_format = '%d-%m-%Y %H:%M:%S'

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Initialize services
entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)
message_service = MessageService(connection)
svc = SeriesService(connection)

title = '\nentity: %s, last hours: %s, minimal score: %s, aggregate period: %s min, interpolate period: %s min, ' \
        'data interval: %s days' % (
    args.entity, args.last_hours, args.min_score, args.aggregate_period, args.interpolate_period, args.data_interval)

if args.metric_filter is None:
    metric_expression = None
else:
    metric_expression = "name like '%s'" % args.metric_filter
    title = '%s, metric filter: %s' % (title, args.metric_filter)

message = [title]

now = datetime.now()

metrics = entities_service.metrics(args.entity, expression=metric_expression,
                                   min_insert_date=now - timedelta(seconds=args.last_hours * 3600),
                                   use_entity_insert_time=True)
log('Processing: ')
for metric in metrics:
    sf = SeriesFilter(metric=metric.name)
    ef = EntityFilter(entity=args.entity)
    df = DateFilter(start_date=datetime(now.year, now.month, now.day) - timedelta(days=args.data_interval),
                    end_date='now')
    tf = TransformationFilter()
    query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)

    if args.aggregate_period > 0:
        tf.set_aggregate(
            Aggregate(period={'count': args.aggregate_period, 'unit': TimeUnit.MINUTE}, types=[AggregateType.MEDIAN]))

    if args.interpolate_period > 0:
        tf.set_interpolate(Interpolate(period={'count': args.interpolate_period, 'unit': TimeUnit.MINUTE},
                                       function=InterpolateFunction.LINEAR))

    query.set_transformation_filter(tf)

    series_list = svc.query(query)
    for series in series_list:
        metric_id = '- %s %s' % (series.metric, print_tags(series.tags))
        log('\t' + metric_id)
        # exclude empty series for specific tags
        if len(series.data) > 2:
            ts = {int(sample.t / 1000): sample.v for sample in series.data}

            detector = AnomalyDetector(ts, score_threshold=args.min_score)

            anomalies = []
            for anomaly in detector.get_anomalies():
                if time.mktime(now.timetuple()) - args.last_hours * 3600 <= anomaly.exact_timestamp:
                    anomalies.append(anomaly)

            if anomalies:
                message.append(metric_id)
                for anomaly in anomalies:
                    t_start, t_end = format_t(anomaly.start_timestamp), format_t(anomaly.end_timestamp)
                    t_exact = format_t(anomaly.exact_timestamp)
                    anomaly_msg = '\tAnomaly from %s to %s with score %s: %s, %s' % (
                        t_start, t_end, anomaly.anomaly_score, t_exact, ts[anomaly.exact_timestamp])
                    message.append(anomaly_msg)

msg = '\n'.join(message)
message_service.insert(Message('anomaly_detection', 'python_script', 'anomaly', now, 'INFO', {}, msg))
print(msg)
