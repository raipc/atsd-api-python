# -*- coding: utf-8 -*-

import time
from datetime import datetime
from atsd_client.models import Entity, Metric, Series, Sample
from service_test_base import ServiceTestBase, MetricsService, SeriesService

NAME = 'pyapi.entity_service.entity'
METRIC = 'pyapi.entity_service.metric'
LABEL = NAME.upper()
INTERPOLATE = 'LINEAR'
TIME_ZONE = 'US/Pacific'
ENABLED = True
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
EXPRESSION = 'name="{}"'.format(NAME)


class TestEntitiesService(ServiceTestBase):

    @classmethod
    def setUpClass(cls):
        """
        Insert series.
        """
        super().setUpClass()
        series = Series(NAME, METRIC)
        series.add_samples(Sample(1, datetime.now()))
        series_service = SeriesService(cls.connection)
        series_service.insert(series)
        time.sleep(cls.wait_time)

    def setUp(self):
        """
        Set entity to initial state.
        """
        entity = Entity(NAME, label=LABEL, interpolate=INTERPOLATE, time_zone=TIME_ZONE, tags=TAGS)
        self.service.create_or_replace(entity)
        time.sleep(self.wait_time)

    def test_fields_match(self):
        """
        Check fields of Entity model were set as expected.
        """
        LAST_INSERT_DATE = datetime.now()
        CREATED_DATE = LAST_INSERT_DATE
        e = Entity(NAME, ENABLED, LABEL, INTERPOLATE, TIME_ZONE, LAST_INSERT_DATE, TAGS, CREATED_DATE)
        self.assertEqual(TAGS, e.tags)
        self.assertEqual(LABEL, e.label)
        self.common_checks(e)

    def test_get(self):
        e = self.service.get(NAME)
        # print(e)
        self.assertIsNotNone(e)
        self.assertEqual(TAGS, e.tags)
        self.assertEqual(LABEL, e.label)
        self.common_checks(e)

    def test_list(self):
        result = self.service.list(expression=EXPRESSION, tags='*')
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        e = result[0]
        self.assertIsNotNone(e)
        self.assertIsInstance(e, Entity)
        self.assertEqual(TAGS, e.tags)
        self.common_checks(e)

    def test_update(self):
        label = "new_label"
        tag_value = "new_tag_value"
        tags = TAGS.copy()
        tags[TAG] = tag_value
        entity = Entity(name=NAME, label=label, tags=tags)
        self.service.update(entity)

        time.sleep(self.wait_time)

        e = self.service.get(NAME)
        # print(e)
        self.assertIsNotNone(e)
        self.assertIsInstance(e, Entity)
        self.assertEqual(tag_value, e.tags[TAG])
        self.assertEqual(label, entity.label)
        self.common_checks(e)

    def test_replace(self):
        """
        Check tags delete.
        """
        entity = Entity(name=NAME)
        self.service.create_or_replace(entity)

        time.sleep(self.wait_time)

        e = self.service.get(NAME)
        # print(e)
        self.assertIsNotNone(e)
        self.assertIsInstance(e, Entity)
        self.assertEqual(NAME, e.name)
        self.assertTrue(e.enabled)
        self.assertDictEqual({}, e.tags)

    def test_metrics(self):
        result = self.service.metrics(entity=NAME, min_insert_date='current_hour')
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        m = result[0]
        self.assertIsNotNone(m)
        self.assertIsInstance(m, Metric)
        self.assertEqual(METRIC, m.name)
        self.assertTrue(m.enabled)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up ATSD.
        """
        cls.service.delete(NAME)
        super().tearDownClass()

    def common_checks(self, entity):
        self.assertEqual(NAME, entity.name)
        self.assertTrue(entity.enabled)
        self.assertEqual(INTERPOLATE, entity.interpolate)
        self.assertEqual(TIME_ZONE, entity.time_zone)
        self.assertTrue(isinstance(entity.last_insert_date, datetime))
        self.assertTrue(isinstance(entity.created_date, datetime))
