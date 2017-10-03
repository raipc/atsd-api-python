from __future__ import print_function

import os
from os import path

from datetime import timedelta, datetime
from dateutil.tz import tzlocal

from atsd_client import connect_url
from atsd_client.services import MetricsService, EntitiesService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
date_to_compare = datetime.now(tzlocal()) - timedelta(days=1)

metrics_service = MetricsService(connection)
metric_list = metrics_service.list(expression="name not like '* *'")
new_metrics = filter(lambda metric: metric.createdDate and metric.createdDate > date_to_compare, metric_list)

entities_service = EntitiesService(connection)
entity_list = entities_service.list()
new_entities = filter(lambda entity: entity.createdDate and entity.createdDate > date_to_compare, entity_list)

with open(os.path.splitext(path.abspath(__file__))[0] + ".txt", 'w') as f:
    print("New metrics and entities created count during the last day (from %s) are %d and %s correspondingly " % (
        date_to_compare.isoformat(), len(new_metrics), len(new_entities)), file=f)
    print(new_metrics, file=f)
    print('---------', file=f)
    print(new_entities, file=f)
    print('---------', file=f)

    new_series = []
    for metric in metric_list:
        series = metrics_service.series(metric, minInsertDate=date_to_compare)
        for s in series:
            if s.lastInsertDate and s.lastInsertDate > date_to_compare:
                new_series.append(s)
                print(s, file=f)

    print("Series count with last insert from the last day (%s) is %d " % (
            date_to_compare.isoformat(), len(new_series)), file=f)



