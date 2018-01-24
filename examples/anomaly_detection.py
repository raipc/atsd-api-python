#!/usr/bin/python3

import argparse
from datetime import timedelta, datetime

import time
from luminol.anomaly_detector import AnomalyDetector

from atsd_client import connect_url
from atsd_client.models import SeriesFilter, EntityFilter, DateFilter, SeriesQuery, TransformationFilter, TimeUnit, \
    Message
from atsd_client.models._meta_models import InterpolateFunction
from atsd_client.services import EntitiesService, MetricsService, SeriesService, MessageService
from atsd_client.utils import print_tags

'''
Find anomaly values through the all series that have at least one value 
during the last hours with minimal score for a given entity. 
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

parser = argparse.ArgumentParser()
parser.add_argument('--last_hours')
parser.add_argument('--min_score')
args = parser.parse_args()

# set entity
entity = '060190011'
grace_interval_days = 14
time_format = '%d-%m-%Y %H:%M:%S'

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)
message_service = MessageService(connection)
svc = SeriesService(connection)

last_hours = float(args.last_hours)
min_score = float(args.min_score)

message = ['entity: %s, last hours: %s, minimal score: %s\n' % (entity, last_hours, min_score)]

# query all metrics for each entity
now = datetime.now()
metrics = entities_service.metrics(entity, min_insert_date=now - timedelta(seconds=last_hours * 3600),
                                   use_entity_insert_time=True)
for metric in metrics:
    sf = SeriesFilter(metric=metric.name)
    ef = EntityFilter(entity=entity)
    df = DateFilter(start_date=datetime(now.year, now.month, now.day) - timedelta(days=grace_interval_days),
                    end_date=now)
    tf = TransformationFilter(
        interpolate={'function': InterpolateFunction.LINEAR, 'period': {'count': 1, 'unit': TimeUnit.HOUR}})

    query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, transformation_filter=tf)
    series_list = svc.query(query)
    for series in series_list:
        # exclude empty series for specific tags
        if series.data:
            ts = {sample.t / 1000: sample.v for sample in series.data}

            detector = AnomalyDetector(ts, score_threshold=min_score)

            anomalies = []
            for anomaly in detector.get_anomalies():
                if now.timestamp() - last_hours * 3600 <= anomaly.exact_timestamp:
                    anomalies.append(anomaly)

            if anomalies:
                metric_id = '%s %s' % (series.metric, print_tags(series.tags))
                message.append(metric_id)
                for anomaly in anomalies:
                    score = anomaly.anomaly_score
                    t_exact = time.strftime(time_format, time.localtime(anomaly.exact_timestamp))
                    t_start = time.strftime(time_format, time.localtime(anomaly.start_timestamp))
                    t_end = time.strftime(time_format, time.localtime(anomaly.end_timestamp))
                    anomaly_msg = '\tAnomaly from %s to %s with score %s: %s, %s' % (
                        t_start, t_end, anomaly.anomaly_score, t_exact, ts[anomaly.exact_timestamp])
                    message.append(anomaly_msg)

msg = '\n'.join(message)
message_service.insert(Message('anomaly_detection', 'python_script', 'anomaly', None, 'INFO', {}, msg))
print(msg)
