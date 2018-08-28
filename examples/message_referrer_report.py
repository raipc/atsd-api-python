#!/usr/bin/env python3
import re
from atsd_client import connect, connect_url
from atsd_client.models import *
from atsd_client.services import *

'''
Query messages matching specified type, source, tags, date interval and convert results into a HTML table.
'''

# Connect to ATSD server
# connection = connect('connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Specify date interval
startDate = "previous_day"
endDate = "current_day"

# Specify message tags
tags = {'http_referer': '*'}

service = MessageService(connection)

# Query the messages and save response to DataFrame with specified columns
ef = EntityFilter(entity="*")
df = DateFilter(start_date=startDate, end_date=endDate)
query = MessageQuery(entity_filter=ef, date_filter=df, type="web", source="access.log", tags=tags, limit=10000)
columns = ['date', 'request_uri', 'http_referer', 'remote_addr', 'geoip_org']
message_frame = service.query_dataframe(query, columns=columns)

# Exclude rows with specified tag values
ignore_hosts = '|'.join(re.escape(s) for s in
    ('google', 'axibase.com', 'yandex.ru', 'baidu.com', 'statcounter.com', 'bing.com', 'duckduckgo.com',
     'jshell.net', 'facebook.com', 't.co', 'dogpile', '78.4'))
ignore_uris = '|'.join(re.escape(s) for s in ('/ec2-monitoring', '/?X'))
filtered = message_frame[(~message_frame['http_referer'].str.contains(ignore_hosts)) &
                         (~message_frame['request_uri'].str.contains(ignore_uris))]
# Rename column names
filtered.columns = ['Date', 'URI', 'Referrer', 'IP', 'Org']

# Avoid `SettingWithCopyWarning`, also pd.set_option('mode.chained_assignment', None) may be used
filtered = filtered.copy()

# Reformat 'Date' column
filtered['Date'] = filtered['Date'].dt.strftime('%Y-%m-%d %H:%M')

# Sort DataFrame by date ascending and convert to HTML table without index column
print(filtered.sort_values(['Date']).to_html(index=False))
