#!/usr/bin/env python

from atsd_client import connect, connect_url
from atsd_client.models import EntityFilter, DateFilter, MessageQuery
from atsd_client.services import MessageService

'''
Query messages matching specified entity, type, source and date interval, group them by specified tag, 
discard groups with count of records less than N and sort remaining groups by date ascending.
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

# Group messages by tag, and filter
grouping_tag = 'geoip_country_code'
N = 1
filtered = messages.groupby(grouping_tag).filter(lambda x: len(x) > N)

# Sort messages by date and tag
sorted = filtered.sort_values([grouping_tag, 'date'])

print(messages)

#                         date       entity        geoip_city geoip_country_code      geoip_region_name
# 0   2018-07-26T17:56:39.303Z  axibase.com             Kazan                 RU              Tatarstan
# 1   2018-07-26T17:55:10.231Z  axibase.com          Helsinki                 FI       Southern Finland
# 2   2018-07-26T17:51:42.308Z  axibase.com            Tandil                 AR           Buenos Aires
# 3   2018-07-26T17:47:17.579Z  axibase.com          L'aquila                 IT                Abruzzi
# 4   2018-07-26T17:45:07.582Z  axibase.com          New York                 US               New York
# 5   2018-07-26T17:41:11.683Z  axibase.com            Athens                 GR                 Attiki
# 6   2018-07-26T17:31:37.156Z  axibase.com        Glen Ellyn                 US               Illinois
# 7   2018-07-26T17:23:12.427Z  axibase.com            Polska                 PL     Kujawsko-Pomorskie
# 8   2018-07-26T17:22:12.387Z  axibase.com             Niles                 US               Michigan
# 9   2018-07-26T17:20:27.015Z  axibase.com  Saint Petersburg                 RU  Saint Petersburg City
# 10  2018-07-26T17:19:20.233Z  axibase.com             Niles                 US               Michigan
# 11  2018-07-26T17:19:15.875Z  axibase.com             Niles                 US               Michigan
# 12  2018-07-26T17:12:42.447Z  axibase.com             Miami                 US                Florida
# 13  2018-07-26T17:05:27.190Z  axibase.com          San Jose                 US             California
# 14  2018-07-26T17:04:09.875Z  axibase.com    Estancia Velha                 BR      Rio Grande do Sul
# 15  2018-07-26T17:03:28.389Z  axibase.com          San Jose                 US             California
# 16  2018-07-26T17:00:04.691Z  axibase.com           Sunbury                 GB                 Surrey
# 17  2018-07-26T17:00:01.901Z  axibase.com        Riemerling                 DE                 Bayern

print(filtered)

#                         date       entity        geoip_city geoip_country_code      geoip_region_name
# 0   2018-07-26T17:56:39.303Z  axibase.com             Kazan                 RU              Tatarstan
# 4   2018-07-26T17:45:07.582Z  axibase.com          New York                 US               New York
# 6   2018-07-26T17:31:37.156Z  axibase.com        Glen Ellyn                 US               Illinois
# 8   2018-07-26T17:22:12.387Z  axibase.com             Niles                 US               Michigan
# 9   2018-07-26T17:20:27.015Z  axibase.com  Saint Petersburg                 RU  Saint Petersburg City
# 10  2018-07-26T17:19:20.233Z  axibase.com             Niles                 US               Michigan
# 11  2018-07-26T17:19:15.875Z  axibase.com             Niles                 US               Michigan
# 12  2018-07-26T17:12:42.447Z  axibase.com             Miami                 US                Florida
# 13  2018-07-26T17:05:27.190Z  axibase.com          San Jose                 US             California
# 15  2018-07-26T17:03:28.389Z  axibase.com          San Jose                 US             California

print(sorted)

#                         date       entity        geoip_city geoip_country_code      geoip_region_name
# 9   2018-07-26T17:20:27.015Z  axibase.com  Saint Petersburg                 RU  Saint Petersburg City
# 0   2018-07-26T17:56:39.303Z  axibase.com             Kazan                 RU              Tatarstan
# 15  2018-07-26T17:03:28.389Z  axibase.com          San Jose                 US             California
# 13  2018-07-26T17:05:27.190Z  axibase.com          San Jose                 US             California
# 12  2018-07-26T17:12:42.447Z  axibase.com             Miami                 US                Florida
# 11  2018-07-26T17:19:15.875Z  axibase.com             Niles                 US               Michigan
# 10  2018-07-26T17:19:20.233Z  axibase.com             Niles                 US               Michigan
# 8   2018-07-26T17:22:12.387Z  axibase.com             Niles                 US               Michigan
# 6   2018-07-26T17:31:37.156Z  axibase.com        Glen Ellyn                 US               Illinois
# 4   2018-07-26T17:45:07.582Z  axibase.com          New York                 US               New York
