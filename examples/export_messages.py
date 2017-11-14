from __future__ import print_function
from __future__ import unicode_literals

from atsd_client import connect_url
from atsd_client.models import EntityFilter, DateFilter, MessageQuery
from atsd_client.services import MessageService
from atsd_client.utils import print_tags

'''
Export messages from ATSD into CSV-file using specified start_date, end_date, type, source and entity.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# set export parameters
start_date = "2017-10-01T00:00:00Z"
end_date = "now"
type = "logger"
source = "com.axibase.tsd.service.search.searchserviceimpl"
entity = "7eacbc4723ed"

message_service = MessageService(connection)

ef = EntityFilter(entity=entity)
df = DateFilter(start_date=start_date, end_date=end_date)
query = MessageQuery(entity_filter=ef, date_filter=df, type=type, source=source)

messages = message_service.query(query)

with open('export.csv', 'w') as f:
    print('date, entity, type, source, severity, tags, message', file=f)
    for message in messages:
        # make message body single line
        msg = message.message.replace("\n", r"\n").replace("\t", r"\t")
        print('%s, %s, %s, %s, %s, %s, %s' % (
            message.date, message.entity, message.type, message.source, message.severity, print_tags(message.tags), msg),
              file=f)
