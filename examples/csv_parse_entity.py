import pandas as pd

from atsd_client import connect
from atsd_client.models import Entity
from atsd_client.services import EntitiesService


def read_csv(path):
    return pd.read_csv(path, sep=',', dtype=str)


# Connect to ATSD

# connection = connect_url('https://atsd_hostname:8443', 'username', 'password')
connection = connect('/path/to/connection.properties')

entities_service = EntitiesService(connection)

df = read_csv('Entity.csv')

fields_dict = {
    'asset_name': 'label',
    'asset_path': 'name'
}
time_zone_dict = {
    'USRI': 'EDT',
    'PRJU': 'PRT'
}
time_zone_field = 'site_is_code'

for index, row in df.where(pd.notnull(df), None).iterrows():
    row_dict = row.to_dict()
    fields_columns = {k: v for k, v in row_dict.iteritems()
                      if k in fields_dict and row_dict[k] is not None}

    entity_params = dict(map(lambda kv: (fields_dict[kv[0]], kv[1]), fields_columns.iteritems()))

    if time_zone_field in row_dict and row_dict[time_zone_field] in time_zone_dict:
        site_code = row_dict[time_zone_field]
        entity_params['time_zone'] = time_zone_dict[site_code]

    entity_params['tags'] = dict(
        {k: v for k, v in row_dict.iteritems() if k not in fields_dict
         and row_dict[k] is not None})
    entity = Entity(**entity_params)
    print entity
    # entities_service.create_or_replace(entity)
