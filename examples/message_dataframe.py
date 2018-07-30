#!/usr/bin/env python

from atsd_client import connect, connect_url
from atsd_client.models import EntityFilter, DateFilter, MessageQuery
from atsd_client.services import MessageService

'''
Query messages matching specified entity, type, source and date interval and convert results into a DataFrame.
'''

# Connect to ATSD server
# connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Set query
entity = "axibase.com"
type = 'web'
source = 'access.log'

# Specify date interval
interval = {"count": 15, "unit": "MINUTE"}
endDate = "NOW"

message_service = MessageService(connection)

# Query the messages and save response to DataFrame
ef = EntityFilter(entity=entity)
df = DateFilter(interval=interval, end_date=endDate)
query = MessageQuery(entity_filter=ef, date_filter=df, type=type, source=source)
messages = message_service.query_dataframe(query, columns=['date', 'entity', 'geoip_city', 'geoip_country_code',
                                                           'geoip_region_name'])

print(messages)

#                        date       entity geoip_city geoip_country_code geoip_region_name
# 0  2018-07-26T17:56:39.303Z  example.org      Kazan                 RU         Tatarstan
# 1  2018-07-26T17:55:10.231Z  example.org   Helsinki                 FI  Southern Finland
# 2  2018-07-26T17:51:42.308Z  example.org     Tandil                 AR      Buenos Aires
# 3  2018-07-26T17:47:17.579Z  example.org   L'aquila                 IT           Abruzzi
# 4  2018-07-26T17:45:07.582Z  example.org   New York                 US          New York
