from __future__ import print_function

import os
from os import path

from atsd_client import connect_url
from atsd_client.services import MetricsService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
metric_service = MetricsService(connection)
metric_list = metric_service.list(expression="name not like '* *'")

required_metrics = [metric for metric in metric_list if metric.lastInsertDate is None]

with open(os.path.splitext(path.abspath(__file__))[0] + ".txt", 'w') as f:
    print("Metrics count: %d, %d without last insert date." % (len(metric_list), len(required_metrics)), file=f)
    for metric in required_metrics:
        print(metric.name, file=f)
