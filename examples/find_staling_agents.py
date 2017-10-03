from __future__ import print_function

import os
from os import path

from datetime import timedelta

from atsd_client import connect_url
from atsd_client.services import MetricsService, EntitiesService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')

agents = ['nurswgvml007', 'nurswgvml010']

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)

with open(os.path.splitext(path.abspath(__file__))[0] + ".txt", 'w') as f:
    for agent in agents:
        entity = entities_service.get(agent)
        date = entity.lastInsertDate
        metrics = entities_service.metrics(entity)
        for metric in metrics:
            series = metrics_service.series(metric, entity)
            for s in series:
                if date - s.lastInsertDate > timedelta(days=1):
                    print(s, file=f)
