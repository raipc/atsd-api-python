from __future__ import print_function

import os
from os import path

from atsd_client import connect_url
from atsd_client.services import MetricsService, EntitiesService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')


entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

entities = entities_service.list(expression="name LIKE '06*'")

with open(os.path.splitext(path.abspath(__file__))[0] + ".txt", 'w') as f:
    for entity in entities:
        metrics = entities_service.metrics(entity)
        for metric in metrics:
            series = metrics_service.series(metric, entity)
            for s in series:
                if s.get_elapsed_minutes() > 24*60:
                    print(s, file=f)
