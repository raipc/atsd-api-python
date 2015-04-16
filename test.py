"""
Copyright 2015 Axibase Corporation or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

https://www.axibase.com/atsd/axibase-apache-2.0.pdf

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""


import sys
import unittest
import time
import random

import atsd_client
from atsd_client import services
from atsd_client import models
from atsd_client.models import TimeUnit
from atsd_client.models import AggregateType
from atsd_client.models import AlertsQuery
from atsd_client.models import AlertHistoryQuery
from atsd_client.models import PropertiesQuery
from atsd_client.models import SeriesQuery
from atsd_client.models import BatchPropertyCommand
from atsd_client.models import BatchAlertCommand
from atsd_client.models import PropertiesMatcher
from atsd_client.models import Series
from atsd_client.models import Property
from atsd_client.models import Metric
from atsd_client.models import Entity
from atsd_client.models import EntityGroup
from atsd_client.models import BatchEntitiesCommand
from atsd_client.exceptions import DataParseException
from atsd_client.exceptions import ServerException


TYPE = 'py.type'
ENTITY = 'py.entity'
METRIC = 'py.metric'
TAG = 'py.tag'
TAG_VALUE = 'py.tag-value'
KEY = 'py.key'
KEY_VALUE = 'py.key-value'
RULE = 'py.rule'
WAIT_TIME = 2
TEST_NAME = 'py.test'
GROUP_NAME = TEST_NAME
ALERT_VALUE = 33333


def get_time_str():
    t = time.localtime()

    tz = (str(int(abs(time.timezone) / 60 / 60)).zfill(2)
          + str(int(abs(time.timezone) / 60 % 60)).zfill(2))
    if time.timezone < 0:
        tz = '-' + tz

    td = {
        'Y': str(t.tm_year),
        'm': str(t.tm_mon),
        'd': str(t.tm_mday),
        'H': str(t.tm_hour),
        'M': str(t.tm_min),
        'S': str(t.tm_sec),
        'z': tz
    }

    return '{Y}-{m}-{d}T{H}:{M}:{S}Z{z}'.format(**td)


def get_timestamp():
    return int(time.time() * 1000)


def get_desired_connection():
    props = open('auth').read().split(',')
    conn = atsd_client.connect_url(base_url=props[0],
                                   username=props[1],
                                   password=props[2])
    return conn


def insert_alert_series_sample(data_service):
    series = Series(ENTITY, METRIC)
    series.add_value(ALERT_VALUE + 1)
    series.tags = {TAG: TAG_VALUE}

    print('insertion =', series)

    return data_service.insert_series(series)


def insert_series_sample(data_service, val=None, *vals):
    if val is None:
        val = random.randint(0, ALERT_VALUE - 1)

    series = Series(ENTITY, METRIC)
    series.tags = {TAG: TAG_VALUE}
    series.add_value(val)
    if vals:
        for i, v in enumerate(vals):
            series.add_value(v, get_timestamp() + i + 1)

    print('insertion =', series)

    return data_service.insert_series(series)


def insert_properties_sample(data_service, tag_value=TAG_VALUE):
    prop = Property(TYPE, ENTITY,
                    tags={TAG: tag_value},
                    key={KEY: KEY_VALUE})

    return data_service.insert_properties(prop)


def query_properties_sample(data_service):
    query = PropertiesQuery(TYPE, ENTITY)
    query.key = {KEY: KEY_VALUE}

    return data_service.retrieve_properties(query)


class TestSeriesService(unittest.TestCase):
    def setUp(self):
        self.svc = services.SeriesService(
            get_desired_connection()
        )

    @unittest.skip("not supported in some environments")
    def test_pandas_support(self):
        query = SeriesQuery(ENTITY, METRIC)
        query.tags = {TAG: [TAG_VALUE]}
        series, = self.svc.retrieve_series(query)

        ts = series.to_pandas_series()
        s = Series.from_pandas_series(ENTITY, METRIC, ts)

        self.assertGreater(str(type(ts)).find('pandas'), 0)
        self.assertIsInstance(s, Series)
        self.assertGreater(str(type(series.plot())), 0)

    def test_series_data_field_empty(self):
        # series with no data
        series = Series(entity=ENTITY,
                        metric=METRIC)
        series.tags = {TAG: TAG_VALUE}
        print(series)

        with self.assertRaises(DataParseException) as cm:
            self.svc.insert_series(series)

        self.assertEqual(cm.exception.non_parsed_field, 'data')

    def test_insert_retrieve_series(self):
        val = random.randint(0, ALERT_VALUE - 1)

        series = Series(ENTITY, METRIC)
        series.tags = {TAG: TAG_VALUE}
        t = get_time_str()
        series.add_value(val, t)

        query = SeriesQuery(ENTITY, METRIC)
        query.tags = {TAG: [TAG_VALUE]}

        successful = self.svc.insert_series(series)
        time.sleep(WAIT_TIME + 2)
        series = self.svc.retrieve_series(query)
        for s in series:
            print(s)

        self.assertTrue(successful)
        self.assertIsNotNone(series)
        self.assertGreater(len(series), 0)

        s = series[0]
        self.assertIsInstance(s, Series)

        data = series[0].data
        self.assertGreater(len(data), 0)
        self.assertEqual(data[-1]['v'], val)

    def test_forecast(self):
        query = SeriesQuery(ENTITY, METRIC)
        query.tags = {TAG: [TAG_VALUE]}
        query.type = models.SeriesType.FORECAST

        series = self.svc.retrieve_series(query)
        self.assertEqual(series[0].type, models.SeriesType.FORECAST)

    def test_rate(self):
        v1 = 5
        v2 = 3
        insert_series_sample(self.svc, v1, v2)
        time.sleep(WAIT_TIME + 2)

        query = SeriesQuery(ENTITY, METRIC)
        query.tags = {TAG: [TAG_VALUE]}
        query.startTime = 1

        rate = query.rate()
        rate.counter = False

        series = self.svc.retrieve_series(query)
        self.assertEqual(int(series[0].data[-1]['v']), v2 - v1)

    def test_group(self):
        time.sleep(1)
        insert_series_sample(self.svc, ALERT_VALUE - 1)
        time.sleep(WAIT_TIME)

        query = SeriesQuery(ENTITY, METRIC)
        query.tags = {TAG: [TAG_VALUE]}
        query.startTime = 1

        group = query.group(AggregateType.COUNT)
        group.set_interval(1, TimeUnit.SECOND)

        series = self.svc.retrieve_series(query)
        self.assertEqual(series[0].data[-1]['v'], 1)

    def test_aggregate_series(self):
        val = random.randint(0, ALERT_VALUE - 1)

        insert_series_sample(self.svc, val)
        time.sleep(WAIT_TIME)

        query = SeriesQuery(ENTITY, METRIC)
        query.tags = {TAG: [TAG_VALUE]}
        query.startTime = 1

        aggr = query.aggregate()
        aggr.set_interval(10, TimeUnit.DAY)
        aggr.set_types(AggregateType.MAX, AggregateType.MIN)

        series = self.svc.retrieve_series(query)
        self.assertEqual(len(series), 2)

        if series[0].aggregate['type'] == 'MAX':
            max = series[0].data[-1]['v']
            min = series[1].data[-1]['v']
        else:
            min = series[0].data[-1]['v']
            max = series[1].data[-1]['v']

        self.assertGreaterEqual(max, min)


class TestPropertiesService(unittest.TestCase):
    def setUp(self):
        self.svc = services.PropertiesService(
            get_desired_connection()
        )

    def test_insert_retrieve_properties(self):
        tag_value = str(random.randint(0, 100))

        tags = {TAG: tag_value}
        prop = Property(TYPE, ENTITY, tags)
        prop.key = {KEY: KEY_VALUE}

        query = PropertiesQuery(TYPE, ENTITY)
        query.startTime = 0
        query.endTime = get_timestamp() + 50000000
        query.key = {KEY: KEY_VALUE}

        successful = self.svc.insert_properties(prop)
        time.sleep(WAIT_TIME)
        properties = self.svc.retrieve_properties(query)
        print(properties)

        self.assertTrue(successful)
        self.assertIsNotNone(properties)
        self.assertGreater(len(properties), 0)
        self.assertIsInstance(properties[0], Property)
        self.assertIn(TAG, properties[0].tags)
        self.assertEqual(tag_value, properties[0].tags[TAG])

    def test_properties_batch_delete_insert(self):
        # ensure properties exists
        insert_properties_sample(self.svc)

        # delete property
        command = BatchPropertyCommand\
            .create_delete_command(TYPE, ENTITY, {KEY: KEY_VALUE})
        successful = self.svc.batch_update_properties(command)

        properties = query_properties_sample(self.svc)

        self.assertTrue(successful)
        self.assertEqual(len(properties), 0)

        tag_value = str(random.randint(0, 100))
        properties = Property(type=TYPE,
                              entity=ENTITY,
                              tags={TAG: tag_value})
        properties.key = {KEY: KEY_VALUE}
        command = BatchPropertyCommand.create_insert_command(properties)
        successful = self.svc.batch_update_properties(command)

        properties = query_properties_sample(self.svc)

        self.assertTrue(successful)
        self.assertGreater(len(properties), 0)
        self.assertEqual(properties[0].tags[TAG], tag_value)

    def test_properties_batch_delete_match(self):
        # remove property
        command = BatchPropertyCommand\
            .create_delete_command(TYPE, ENTITY, {KEY: KEY_VALUE})
        self.svc.batch_update_properties(command)
        time.sleep(WAIT_TIME)

        timestamp = get_timestamp()
        time.sleep(2)

        # create insertion template without timestamp
        insertion = Property(TYPE, ENTITY, None,
                             key={KEY: KEY_VALUE})

        # delete-match command
        matcher = PropertiesMatcher(type=TYPE)
        matcher.createdBeforeTime = timestamp + 1000
        command = BatchPropertyCommand.create_delete_match_command(matcher)

        # insert properties timestamp < createdBeforeTime
        insertion.timestamp = timestamp
        insertion.tags = {TAG: 'before'}
        self.svc.insert_properties(insertion)

        # insert properties timestamp > createdBeforeTime
        insertion.timestamp = timestamp + 2000
        insertion.tags = {TAG: 'after'}
        self.svc.insert_properties(insertion)

        successful = self.svc.batch_update_properties(command)
        time.sleep(WAIT_TIME)
        properties = query_properties_sample(self.svc)
        print(properties)

        self.assertTrue(successful)
        self.assertGreater(len(properties), 0)
        self.assertEqual(properties[0].tags[TAG], 'after')


class TestAlertsService(unittest.TestCase):
    def setUp(self):
        conn = get_desired_connection()

        self.svc = services.AlertsService(conn)

        # fire alert
        series_svc = services.SeriesService(conn)
        insert_alert_series_sample(series_svc)
        time.sleep(WAIT_TIME)

    def test_retrieve_alerts(self):
        query = AlertsQuery(entities=[ENTITY], metrics=[METRIC])
        alerts = self.svc.retrieve_alerts(query)
        print(alerts)

        self.assertIsNotNone(alerts)
        self.assertEqual(len(alerts), 1)
        self.assertFalse(alerts[0].acknowledged)

    def test_retrieve_alert_history(self):
        query = AlertHistoryQuery(metric=METRIC,
                                  entity=ENTITY,
                                  startTime=get_timestamp() - 100000000,
                                  endTime=get_timestamp(),
                                  rule=RULE)
        alert_history = self.svc.retrieve_alert_history(query)
        print(alert_history)

        self.assertIsNotNone(alert_history)
        self.assertGreater(len(alert_history), 0)

    def test_update_alerts(self):
        query = AlertsQuery(metrics=[METRIC],
                            entities=[ENTITY],
                            rules=[RULE])

        alerts = self.svc.retrieve_alerts(query)

        # set all acknowledged
        command = BatchAlertCommand.create_update_command(
            True, *[a.id for a in alerts]
        )
        self.svc.batch_update_alerts(command)

        alerts = self.svc.retrieve_alerts(query)

        is_all_acknowledged = True
        for alert in alerts:
            is_all_acknowledged = is_all_acknowledged and alert.acknowledged

        self.assertTrue(is_all_acknowledged)

        # clean alerts
        query = AlertsQuery(entities=[ENTITY], metrics=[METRIC])
        alerts = self.svc.retrieve_alerts(query)
        command = BatchAlertCommand.create_delete_command(
            *[a.id for a in alerts])
        successful = self.svc.batch_update_alerts(command)

        alerts = self.svc.retrieve_alerts(query)
        self.assertTrue(successful)
        self.assertEqual(len(alerts), 0)


class TestMetricsService(unittest.TestCase):
    def setUp(self):
        self.svc = services.MetricsService(
            get_desired_connection()
        )
        metric = Metric(TEST_NAME, tags={'table': 'py.test'})
        self.svc.create_or_replace_metric(metric)
        time.sleep(WAIT_TIME)

    def test_retrieve_metrics(self):
        metrics = self.svc.retrieve_metrics(
            tags='*',
            expression='tags.table like "py*est"'
        )
        print(metrics)

        self.assertIsNotNone(metrics)
        self.assertGreater(len(metrics), 0)
        self.assertIsInstance(metrics[0], Metric)
        self.assertIn('table', metrics[0].tags)
        self.assertEqual(metrics[0].tags['table'], 'py.test')
        self.assertEqual(metrics[0].name, TEST_NAME)

    def test_retrieve_metric(self):
        metric = self.svc.retrieve_metric(TEST_NAME)

        self.assertIsInstance(metric, Metric)
        self.assertEqual(metric.name, TEST_NAME)

        non_exists_name = 'not-a-metric' + str(random.randint(0, 1000))
        metric = self.svc.retrieve_metric(non_exists_name)

        self.assertIsNone(metric)

    def test_replace_metric(self):
        metric = self.svc.retrieve_metric(TEST_NAME)

        print(metric)
        old_counter = metric.counter
        metric.counter = not old_counter
        successful = self.svc.create_or_replace_metric(metric)

        metric = self.svc.retrieve_metric(TEST_NAME)

        self.assertTrue(successful)
        self.assertIsNotNone(metric)
        self.assertEqual(metric.name, TEST_NAME)
        self.assertNotEqual(old_counter, metric.counter)

    def test_update_metric(self):
        metric = self.svc.retrieve_metric(TEST_NAME)

        old_tag = metric.tags['table']
        new_tag = 'new_' + old_tag

        # update tag
        metric.tags = {'table': new_tag}
        self.svc.update_metric(metric)
        metric = self.svc.retrieve_metric(TEST_NAME)
        print(metric)

        self.assertEqual(metric.tags['table'], new_tag)

        del metric.tags
        self.svc.update_metric(metric)
        metric = self.svc.retrieve_metric(TEST_NAME)
        self.assertEqual(metric.tags['table'], new_tag)

    def test_delete_create_metric(self):
        metric = Metric(TEST_NAME)
        successful = self.svc.delete_metric(metric)

        self.assertTrue(successful)
        self.assertIsNone(self.svc.retrieve_metric(TEST_NAME))

        successful = self.svc.create_or_replace_metric(metric)

        self.assertTrue(successful)
        self.assertIsNotNone(self.svc.retrieve_metric(TEST_NAME))


class TestEntitiesService(unittest.TestCase):
    def setUp(self):
        self.svc = services.EntitiesService(
            get_desired_connection()
        )
        entity = Entity(TEST_NAME, tags={'environment': 'py.test'})
        self.svc.create_or_replace_entity(entity)
        time.sleep(WAIT_TIME)

    def test_retrieve_entities(self):
        entities = self.svc.retrieve_entities(
            tags='*',
            expression='tags.environment like "py*est"'
        )
        print(entities)

        self.assertIsNotNone(entities)
        self.assertGreater(len(entities), 0)
        self.assertIsInstance(entities[0], Entity)
        self.assertIn('environment', entities[0].tags)
        self.assertEqual(entities[0].tags['environment'], 'py.test')
        self.assertEqual(entities[0].name, TEST_NAME)

    def test_retrieve_entity(self):
        entity = self.svc.retrieve_entity(TEST_NAME)

        self.assertIsInstance(entity, Entity)
        self.assertEqual(entity.name, TEST_NAME)

        non_exists_name = 'not-an-entity' + str(random.randint(0, 1000))
        entity = self.svc.retrieve_entity(non_exists_name)

        self.assertIsNone(entity)

    def test_replace_entity(self):
        entity = self.svc.retrieve_entity(TEST_NAME)
        print(entity)

        del entity.tags
        successful = self.svc.create_or_replace_entity(entity)
        entity = self.svc.retrieve_entity(TEST_NAME)
        print(entity)

        self.assertTrue(successful)
        self.assertNotIn('environment', entity.tags)

    def test_update_entity(self):
        # bug in atsd < 8669
        entity = self.svc.retrieve_entity(TEST_NAME)

        old_tag = entity.tags['environment']
        new_tag = 'new_' + old_tag

        # update tag
        entity.tags = {'environment': new_tag}
        self.svc.update_entity(entity)
        entity = self.svc.retrieve_entity(TEST_NAME)
        print(entity)

        self.assertEqual(entity.tags['environment'], new_tag)

        del entity.tags
        self.svc.update_entity(entity)
        entity = self.svc.retrieve_entity(TEST_NAME)
        self.assertEqual(entity.tags['environment'], new_tag)

    def test_delete_create_entity(self):
        entity = Entity(TEST_NAME)
        successful = self.svc.delete_entity(entity)

        self.assertTrue(successful)
        self.assertIsNone(self.svc.retrieve_entity(TEST_NAME))

        successful = self.svc.create_or_replace_entity(entity)

        self.assertTrue(successful)
        self.assertIsNotNone(self.svc.retrieve_entity(TEST_NAME))


class TestEntityGroupsService(unittest.TestCase):
    def setUp(self):
        conn = get_desired_connection()
        self.svc = services.EntityGroupsService(conn)

        group = EntityGroup(GROUP_NAME, tags={'pytag': 'py.test'})
        self.svc.create_or_replace_entity_group(group)
        self.svc.add_group_entities(GROUP_NAME, Entity(TEST_NAME))
        time.sleep(WAIT_TIME)

    def test_retrieve_entity_groups(self):
        groups = self.svc.retrieve_entity_groups(
            tags='*',
            expression='tags.pytag like "py*est"'
        )
        print(groups)

        self.assertIsNotNone(groups)
        self.assertGreater(len(groups), 0)
        self.assertIsInstance(groups[0], EntityGroup)
        self.assertIn('pytag', groups[0].tags)
        self.assertEqual(groups[0].tags['pytag'], 'py.test')
        self.assertEqual(groups[0].name, GROUP_NAME)

    def test_retrieve_entity_group(self):
        group = self.svc.retrieve_entity_group(GROUP_NAME)

        self.assertIsInstance(group, EntityGroup)
        self.assertEqual(group.name, GROUP_NAME)

        non_exists_name = 'not-a-group' + str(random.randint(0, 1000))
        group = self.svc.retrieve_entity_group(non_exists_name)

        self.assertIsNone(group)

    def test_replace_entity_group(self):
        group = self.svc.retrieve_entity_group(GROUP_NAME)
        print(group)

        del group.tags
        successful = self.svc.create_or_replace_entity_group(group)
        group = self.svc.retrieve_entity_group(GROUP_NAME)
        print(group)

        self.assertTrue(successful)
        self.assertNotIn('pytag', group.tags)

    def test_update_entity_group(self):
        group = self.svc.retrieve_entity_group(GROUP_NAME)

        old_tag = group.tags['pytag']
        new_tag = 'new_' + old_tag

        # update tag
        group.tags = {'pytag': new_tag}
        self.svc.update_entity_group(group)
        group = self.svc.retrieve_entity_group(TEST_NAME)
        print(group)

        self.assertEqual(group.tags['pytag'], new_tag)

        del group.tags
        self.svc.update_entity_group(group)
        group = self.svc.retrieve_entity_group(GROUP_NAME)
        self.assertEqual(group.tags['pytag'], new_tag)

    def test_delete_create_entity_group(self):
        group = EntityGroup(GROUP_NAME)
        successful = self.svc.delete_entity_group(group)

        self.assertTrue(successful)
        self.assertIsNone(self.svc.retrieve_entity_group(GROUP_NAME))

        successful = self.svc.create_or_replace_entity_group(group)

        self.assertTrue(successful)
        self.assertIsNotNone(self.svc.retrieve_entity_group(GROUP_NAME))

    def test_retrieve_group_entities(self):
        entities = self.svc.retrieve_group_entities(GROUP_NAME)
        print(entities)

        self.assertIsNotNone(entities)
        self.assertGreater(len(entities), 0)
        self.assertIsInstance(entities[0], Entity)

    def test_add_delete_group_entities(self):
        entities = self.svc.retrieve_group_entities(GROUP_NAME)
        entity_names = [e.name for e in entities]
        successful = self.svc.delete_group_entities(GROUP_NAME, *entity_names)
        entities = self.svc.retrieve_group_entities(GROUP_NAME)

        self.assertTrue(successful)
        self.assertEqual(len(entities), 0)

        successful = self.svc.add_group_entities(GROUP_NAME, Entity(TEST_NAME))
        entities = self.svc.retrieve_group_entities(GROUP_NAME)

        self.assertTrue(successful)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].name, TEST_NAME)

    def test_group_entities_batch_commands(self):
        not_entity_name = 'py.not-exists'

        add = BatchEntitiesCommand.create_add_command(Entity(TEST_NAME))
        add_non_exist = BatchEntitiesCommand.create_add_command(
            Entity(not_entity_name),
            createEntities=False
        )
        delete = BatchEntitiesCommand.create_delete_command(TEST_NAME)
        delete_all = BatchEntitiesCommand.create_delete_all_command()

        successful = self.svc \
            .batch_update_group_entities(GROUP_NAME, delete_all)
        entities = self.svc.retrieve_group_entities(GROUP_NAME)
        self.assertTrue(successful)
        self.assertEqual(len(entities), 0)

        with self.assertRaises(ServerException):
            successful = self.svc \
                .batch_update_group_entities(GROUP_NAME, add, add_non_exist)

        entities = self.svc.retrieve_group_entities(GROUP_NAME)
        self.assertTrue(successful)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].name, TEST_NAME)

        successful = self.svc \
            .batch_update_group_entities(GROUP_NAME, delete)
        entities = self.svc.retrieve_group_entities(GROUP_NAME)
        self.assertTrue(successful)
        self.assertEqual(len(entities), 0)


if __name__ == '__main__':
    print('python version: ', sys.version, '\n')
    unittest.main()