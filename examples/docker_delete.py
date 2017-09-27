#!/usr/bin/env python
import os
import pprint
import time

import sys

from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from dateutil.tz import tzlocal

import logging
from atsd_client import connect
from atsd_client.services import EntitiesService, MetricsService

'''
Locate a collection of entities (docker hosts in this cases).
Delete those that have not inserted data for more than 4 days
Also delete related entities (docker containers).
Connection.properties will be taken from the same folder where script is.
'''

logging.getLogger().setLevel(logging.INFO)

os.environ['TZ'] = 'Europe/London'
time.tzset()

tags_printer = pprint.PrettyPrinter(indent=4)
conn = connect()
#conn = connect_url('https://atsd_hostname:8443', 'user', 'pwd')
#conn = atsd_client.connect('/home/axibase/connection.properties')

entity_service = EntitiesService(conn)
metric_service = MetricsService(conn)

# select all entities that collect this metric
# this metric is collected by docker hosts
docker_hosts = metric_service.series('docker.cpu.sum.usage.total.percent')

print("Docker hosts found: " + str(len(docker_hosts)))

for docker_host_series in docker_hosts:
    print("--------------")

    # convert lastInsertDate to `datetime.datetime` object
    last_insert_time = parse_date(docker_host_series.lastInsertDate)

    # calculate time difference between now and last insert time
    elapsed_time = datetime.now(tzlocal()) - last_insert_time

    # days since last insert, rounded down to nearest integer
    elapsed_days = int(elapsed_time.days)

    entity_filter = "lower(tags.docker-host) = lower('" + docker_host_series.entity + "')"
    # find related entities, which tag value equals docker host
    entities = entity_service.list(expression=entity_filter, limit=0, tags="*")

    print(" - FOUND " + str(len(entities)) + " objects for docker_host= " + docker_host_series.entity +
          " : " + docker_host_series.lastInsertDate + " : elapsed_days= " + str(elapsed_days))

    # keep entitites that have recent data (inserted within the last 7 days)
    if elapsed_time < timedelta(hours=7*24):
        print(" - RETAIN (do not delete): " + docker_host_series.entity)
        continue

    print(" - DELETE objects for docker_host= " + docker_host_series.entity)

    for entity in entities:

        if entity.name == docker_host_series.entity:
            #ignore the docker host itself, it will be deleted later
            continue;

        print("- Deleting " + entity.tags.get('docker-type', '') + " : " + entity.name + " : " + entity.tags.get('name', ''))
        tags_printer.pprint(entity.tags)
        # Uncomment next line to delete
        # entity_service.delete(entity)

    print("- DELETE Docker host: " + docker_host_series.entity)
    # Uncomment next line to delete
    # entity_service.delete(docker_host_series.entity)
