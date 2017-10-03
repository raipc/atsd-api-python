from __future__ import print_function

import os
from os import path

from datetime import datetime, timedelta
from dateutil.tz import tzlocal

from atsd_client import connect_url
from atsd_client.services import MetricsService

date_to_compare = datetime.now(tzlocal()) - timedelta(days=30)

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
metrics_service = MetricsService(connection)
metric_list = metrics_service.list(expression="name not like '* *'")

required_metrics = [metric for metric in metric_list if
                    metric.createdDate is not None and metric.createdDate > date_to_compare]
with open(os.path.splitext(path.abspath(__file__))[0] + ".txt", 'w') as f:
    print("Metrics created later than %s" % (date_to_compare.isoformat()), file=f)
    print(required_metrics, file=f)
