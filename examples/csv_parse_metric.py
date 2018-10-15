import pandas as pd

from atsd_client import connect
from atsd_client.models import Metric
from atsd_client.services import MetricsService


def read_csv(path):
    return pd.read_csv(path, sep=',', dtype=str)


# Connect to ATSD

# connection = connect_url('https://atsd_hostname:8443', 'username', 'password')
connection = connect('/path/to/connection.properties')
metric_service = MetricsService(connection)

df = read_csv('Metric.csv')

fields_dict = {
    'tag_name': 'name',
    'attribute_name': 'label',
    'tag_description': 'description',
    'tag_value_type': 'data_type',
    'uom_long': 'units',
    'step': 'interpolate',
    'zero': 'min_value',
    'span': 'max_value'
}

fields_transformations = {
    'step': lambda r: 'LINEAR' if r['step'] == 0 else 'PREVIOUS',
    'tag_value_type': lambda r: 'DOUBLE' if r['tag_value_type'] == 'Double' else 'FLOAT'
    if r['tag_value_type'] == 'Single' else 'LONG',
    'span': lambda r: float(r['zero']) + float(r['span'])
}


def transform_field(r):
    def transform(kv):
        column_name = kv[0]
        field_name = fields_dict[column_name]
        cell_value = kv[1]
        if column_name in fields_transformations:
            return field_name, fields_transformations[column_name](r)
        else:
            return field_name, cell_value

    return transform


for index, row in df.where(pd.notnull(df), None).iterrows():
    row_dict = row.to_dict()
    tag_name = row_dict['tag_name']
    if tag_name is not None:
        if "%" in tag_name:
            print 'Metric {metric} contains illegal character and will be ignored.'.format(metric=tag_name)
            continue
        fields_columns = {k: v for k, v in row_dict.iteritems()
                          if k in fields_dict and row_dict[k] is not None}

        metric_params = dict(map(transform_field(fields_columns), fields_columns.iteritems()))

        metric_params['tags'] = dict(
            {k: v for k, v in row_dict.iteritems() if k not in fields_dict
             and row_dict[k] is not None})

        metric = Metric(**metric_params)
        print metric
        # metric_service.create_or_replace(metric)
