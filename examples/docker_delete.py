#!/usr/bin/env python
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
import pprint

from atsd_client import connect_url
from atsd_client.services import EntitiesService
from atsd_client.models import Entity
import pytz

'''
Locate a collection of entities (docker hosts in this cases).
Delete those that have not inserted data for more than 4 days
Also delete related entities (docker containers).
'''

tags_printer = pprint.PrettyPrinter(indent=4)
conn = connect_url('http://atsd_hostname:8088', 'user', 'pwd')
#conn = atsd_client.connect('/home/axibase/connection.properties')

entity_service = EntitiesService(conn)

# select all entities that collect this metric
# this metric is collected by docker hosts
docker_hosts = conn.get("v1/metrics/docker.cpu.sum.usage.total.percent/series")

print("Docker hosts found: " + str(len(docker_hosts)))

for el in docker_hosts:
    docker_host = Entity(el["entity"])
    docker_host.lastInsertDate = el["lastInsertDate"]
    print("--------------")

    # convert all times to UTC timezone
    last_insert_time = parse_date(docker_host.lastInsertDate).replace(tzinfo=pytz.utc)

    # calculate time difference between now and last insert time
    elapsed_time = datetime.now(pytz.utc) - last_insert_time

    # days since last insert, rounded down to nearest integer
    elapsed_days = int(elapsed_time.days)

    entity_filter = "lower(tags.docker-host) = lower('" + docker_host.name + "')"
    # find related entities, which tag value equals docker host
    entities = entity_service.list(expression=entity_filter, limit=0, tags="*")

    print(" - FOUND " + str(len(entities)) + " objects for docker_host= " + docker_host.name +
          " : " + docker_host.lastInsertDate + " : elapsed_days= " + str(elapsed_days))

    # keep entitites that have recent data (inserted within the last 7 days)
    if elapsed_time < timedelta(hours=7*24):
        print(" - RETAIN (do not delete): " + docker_host.name)
        continue

    print(" - DELETE objects for docker_host= " + docker_host.name)

    for entity in entities:
        
        if entity.name == docker_host.name:
            #ignore the docker host itself, it will be deleted later
            continue;
            
        print("- Deleting " + entity.tags.get('docker-type', '') + " : " + entity.name + " : " + entity.tags.get('name', ''))
        tags_printer.pprint(entity.tags)
        # Uncomment next line to delete
        #entity_service.delete(entity)

    print("- DELETE Docker host: " + docker_host.name)
    # Uncomment next line to delete
    #entity_service.delete(docker_host)
