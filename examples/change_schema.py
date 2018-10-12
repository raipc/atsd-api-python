# Create client for old-schema client
from string import Template

from atsd_client import connect_url
from atsd_client.services import SQLService, CommandsService

old_db_connection = connect_url('atsd_hostname', 'user', 'password')

sql_service = SQLService(old_db_connection)
metric_name = "metric_name"

sql_query = 'SELECT entity,metric, value, text, datetime, tags.* FROM "' + metric_name + '"'

transformed_commands = []

for index, row in sql_service.query(sql_query).iterrows():
    row_dict = row.to_dict()
    filtered_row = {k: v for k, v in row_dict.iteritems()
                    if v and not (v == 1 and k == 'tags._index') and k != 'tags.time_zone'
                    and not (v == 0 and k == 'tags.status')}
    tags = {k: v for k, v in filtered_row.iteritems()
            if k.startswith('tags.')}
    series = {k: v for k, v in filtered_row.iteritems()
              if not k.startswith('tags.')}
    command = Template('series e:$metric m:$entity=$value x:$entity=$text d:$datetime').safe_substitute(series) + \
              "".join(map(lambda x: ' t:' + x + '=' + str(tags[x]), tags.keys()))
    transformed_commands.append(command)

new_db_connection = connect_url('atsd_hostname', 'user', 'password')

command_service = CommandsService(new_db_connection)

for command in transformed_commands:
    print command

# command_service.send_commands(transformed_commands)
