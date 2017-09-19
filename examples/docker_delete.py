import atsd_client
import dateutil.parser
import datetime
import pytz
import pprint

pp = pprint.PrettyPrinter(indent=4)
conn = atsd_client.connect_url('http://atsd_hostname:8088', 'user', 'pwd')
#conn = atsd_client.connect('/home/axibase/connection.properties')

from atsd_client.services import EntitiesService
from atsd_client.models import Entity
entity_service = EntitiesService(conn)
docker_hosts = conn.get("v1/metrics/docker.cpu.sum.usage.total.percent/series")

print("Docker hosts found: " + str(len(docker_hosts)))

for el in docker_hosts:
	docker_host = Entity(el["entity"])
	docker_host.lastInsertDate = el["lastInsertDate"]
	print("--------------")

	lastInsertTime = dateutil.parser.parse(docker_host.lastInsertDate).replace(tzinfo=pytz.utc)
	elapsedTime = datetime.datetime.now(pytz.utc) - lastInsertTime
	elapsed_days = round(elapsedTime.total_seconds()/(24*3600),1)

	entityFilter = "lower(tags.docker-host) = lower('" + docker_host.name + "')"	
	entities = entity_service.list(expression=entityFilter, limit=0, tags="*")	

	print(" - FOUND " + str(len(entities)) + " objects for docker_host= " + docker_host.name + " : " + docker_host.lastInsertDate + " : elapsed_days= " + str(elapsed_days))

	if (elapsed_days) < 7:
		print(" - RETAIN (do not delete): " + docker_host.name)
		continue

	print(" - DELETE objects for docker_host= " + docker_host.name)

	for entity in entities:
		print("- Deleting " + entity.tags.get('docker-type','') + " : " + entity.name + " : " + entity.tags.get('name',''))
		pp.pprint(entity.tags)
		# Uncomment next line to delete
		#entity_service.delete(entity)

	print("- DELETE Docker host: " + docker_host.name)
	# Uncomment next line to delete
	#entity_service.delete(docker_host)
