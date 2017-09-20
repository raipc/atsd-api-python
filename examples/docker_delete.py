from datetime import datetime
from dateutil.parser import parse as parse_date
import pprint

from atsd_client import connect_url
from atsd_client.services import EntitiesService
from atsd_client.models import Entity
import pytz


tags_printer = pprint.PrettyPrinter(indent=4)
conn = connect_url('http://atsd_hostname:8088', 'user', 'pwd')
#conn = atsd_client.connect('/home/axibase/connection.properties')

entity_service = EntitiesService(conn)
docker_hosts = conn.get("v1/metrics/docker.cpu.sum.usage.total.percent/series")

print("Docker hosts found: {}".format(len(docker_hosts)))

for el in docker_hosts:
    docker_host = Entity(el["entity"])
    docker_host.lastInsertDate = el["lastInsertDate"]
    print("--------------")

    last_insert_time = parse_date(docker_host.lastInsertDate).replace(tzinfo=pytz.utc)
    elapsed_time = datetime.now(pytz.utc) - last_insert_time
    elapsed_days = round(elapsed_time.total_seconds() / (24 * 3600), 1)

    entity_filter = "lower(tags.docker-host) = lower('" + docker_host.name + "')"
    entities = entity_service.list(expression=entity_filter, limit=0, tags="*")

    print(" - FOUND {} objects for docker_host={} : {} : elapsed_days={}".format(len(entities), docker_host.name, docker_host.lastInsertDate, elapsed_days))

    if elapsed_days < 7:
        print(" - RETAIN (do not delete): " + docker_host.name)
        continue

    print(" - DELETE objects for docker_host= " + docker_host.name)

    for entity in entities:
        print("- Deleting {} : {} : {}".format(entity.tags.get('docker-type',''), entity.name, entity.tags.get('name','')))
        tags_printer.pprint(entity.tags)
        # Uncomment next line to delete
        #entity_service.delete(entity)

    print("- DELETE Docker host: " + docker_host.name)
    # Uncomment next line to delete
    #entity_service.delete(docker_host)
