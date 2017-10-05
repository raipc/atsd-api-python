from __future__ import print_function

import os
from os import path

from datetime import timedelta

from atsd_client import connect_url
from atsd_client.services import MetricsService, EntitiesService

connection = connect_url('https://atsd_hostname:8443', 'user', 'pwd')

entities_service = EntitiesService(connection)
metrics_service = MetricsService(connection)
entities = filter(lambda entity: entity.lastInsertDate is not None, entities_service.list(limit=100))

with open(os.path.splitext(path.abspath(__file__))[0] + ".txt", 'w') as f:
    for entity in entities:
        metrics = entities_service.metrics(entity.name)
        for m in metrics:
            specific_series = metrics_service.series(m.name, entity.name)
            if len(specific_series) > 1:
                # find one day lag
                lower_limit_date = max(s.lastInsertDate for s in specific_series) - timedelta(days=1)
                for ss in specific_series:
                    if ss.lastInsertDate < lower_limit_date:
                        print(ss, file=f)
