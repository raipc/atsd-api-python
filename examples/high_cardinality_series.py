from __future__ import print_function

import os
from os import path

from atsd_client import connect_url
from atsd_client.services import MetricsService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
metrics_service = MetricsService(connection)
metric_list = metrics_service.list(expression="name not like '* *'")
metrics_with_last_insert = filter(lambda metric: metric.lastInsertDate is not None, metric_list)

cardinality = 8

required_series = []

for metric in metrics_with_last_insert:
    series_list = metrics_service.series(metric)
    for s in series_list:
        if len(s.tags) > cardinality:
            required_series.append(s)

with open(os.path.splitext(path.abspath(__file__))[0] + ".txt", 'w') as f:
    print("Series that have more than %d tags combinations" % (cardinality), file=f)
    print(required_series, file=f)
