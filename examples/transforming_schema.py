# Create client for old-schema client
import json
from string import Template

from atsd_client import connect_url
from atsd_client.services import SQLService, CommandsService


def read_config(filename):
    """Read configuration from json file
        :param filename path to config file
    """
    with open(filename, 'r') as f:
        return json.load(f)


def connection_from_config(conn):
    """
    Create connection from connection configuration
        :param conn connection configuration
    """
    return connect_url(conn['url'], conn['username'], conn['password'])


def tags_filter_from_config(config):
    """
    Create tags filter form configuration
        :param config tags_filter configuration
    """

    def filter_dict(kv):
        keys_to_remove = config['keys_to_remove']
        values_to_remove = config['values_to_remove']
        default_tags_values = config['default_tags_values']
        return not (kv[0] in keys_to_remove) and \
               not kv[1] in values_to_remove and \
               not (default_tags_values.has_key(kv[0]) and default_tags_values[kv[0]] == kv[1])

    return filter_dict


def row_transformation(series_tags_filter):
    """Transform query row to new series command with specified series_tags_filter
    :param series_tags_filter:
    :return:
    """

    def transformation(i_row):
        row_dict = i_row[1].to_dict()

        # transforming
        """
        * Swap entity and metric
        * Discard tags that contain false values
        * Discard time_zone tag
        * Discard _index tag if it is equal 1
        * Discard status tag if it is equal 0
        """

        # stores fixed series fields
        series = {k: v for k, v in row_dict.iteritems()
                  if not k.startswith('tags.')}

        # stores series tags
        tags_columns = {k: v for k, v in row_dict.iteritems() if k.startswith('tags.')}
        tags = dict(map(lambda kv: (kv[0].replace("tags.", ""), kv[1]), tags_columns.iteritems()))
        filtered_tags = dict(filter(series_tags_filter, tags.iteritems()))

        # Generate command to insert in new db
        return Template('series e:$metric m:$entity=$value x:$entity=$text d:$datetime').safe_substitute(series) + \
               "".join(map(lambda x: ' t:' + x + '=' + str(tags[x]), filtered_tags.keys()))

    return transformation


app_config = read_config('transform-schema-config.json')

# Setup connection to source db
source_db_connection = connection_from_config(app_config['connection']['source'])
sql_service = SQLService(source_db_connection)

# transformation config
transformation_config = app_config['transformation']
metric_name = transformation_config['metric']

# query all series for metric
sql_query = 'SELECT entity,metric, value, text, datetime, tags.* FROM "' + metric_name + '"'
query_result = sql_service.query(sql_query)

# Generate transformed commands
tags_filter = tags_filter_from_config(transformation_config['tags_filter'])
transformed_commands = list(map(row_transformation(tags_filter), query_result.iterrows()))

# Send generated commands to target db
new_db_connection = connection_from_config(app_config['connection']['target'])
command_service = CommandsService(new_db_connection)
for command in transformed_commands:
    print command

# command_service.send_commands(transformed_commands)
