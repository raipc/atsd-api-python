# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime
from atsd_client.models import Metric, Series, Sample
from service_test_base import ServiceTestBase, SeriesService

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.metrics_service.entity'
NAME = 'pyapi.metrics_service.metric'
LABEL = NAME.upper()
INTERPOLATE = 'LINEAR'
TIME_ZONE = 'HST'
ENABLED = True
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
DATA_TYPE = "DECIMAL"
PERSISTENT = True
FILTER = 'name="{}"'.format(NAME)
MIN_VALUE = -1
MAX_VALUE = 100
INVALID_ACTION = "TRANSFORM"
DESCRIPTION = "Test metric for Python client MetricsService."
RETENTION_DAYS = 5
SERIES_RETENTION_DAYS = 4
VERSIONED = False
UNITS = "km"


class TestMetricsService(ServiceTestBase):

    def setUp(self):
        """
        Set metric to initial state.
        """
        m = Metric(NAME, LABEL, ENABLED, DATA_TYPE, PERSISTENT, FILTER, MIN_VALUE, MAX_VALUE, INVALID_ACTION,
                   DESCRIPTION, RETENTION_DAYS, SERIES_RETENTION_DAYS, tags=TAGS,
                   interpolate=INTERPOLATE, units=UNITS, time_zone=TIME_ZONE)
        self.service.create_or_replace(m)
        time.sleep(self.wait_time)

    def test_fields_match(self):
        """
        Check fields of Metric model were set as expected.
        """
        LAST_INSERT_DATE = datetime.now()
        CREATED_DATE = LAST_INSERT_DATE
        m = Metric(NAME, LABEL, ENABLED, DATA_TYPE, PERSISTENT, FILTER, MIN_VALUE, MAX_VALUE, INVALID_ACTION,
                   DESCRIPTION, RETENTION_DAYS, SERIES_RETENTION_DAYS, LAST_INSERT_DATE, TAGS,
                   VERSIONED, INTERPOLATE, UNITS, TIME_ZONE, CREATED_DATE)
        self.assertEqual(TAGS, m.tags)
        self.assertEqual(LABEL, m.label)
        self.assertTrue(isinstance(m.last_insert_date, datetime))
        self.common_checks(m)

    def test_get(self):
        m = self.service.get(NAME)

        # print(m)
        self.assertEqual(TAGS, m.tags)
        self.assertEqual(LABEL, m.label)
        self.common_checks(m)

    def test_list(self):
        result = self.service.list(expression=FILTER, tags='*')

        # print(result)

        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        m = result[0]
        self.assertEqual(TAGS, m.tags)
        self.assertEqual(LABEL, m.label)
        self.common_checks(m)

    def test_update(self):
        label = "new_label"
        tag_value = "new_tag_value"
        tags = TAGS.copy()
        tags[TAG] = tag_value
        metric = Metric(name=NAME, label=label, tags=tags)
        self.service.update(metric)

        time.sleep(self.wait_time)

        m = self.service.get(NAME)
        # print(m)
        self.common_checks(m)

    def test_replace(self):
        """
        Check tags and fields delete.
        """
        metric = Metric(name=NAME)
        self.service.create_or_replace(metric)

        time.sleep(self.wait_time)

        m = self.service.get(NAME)
        # print(e)
        self.assertIsNotNone(m)
        self.assertIsInstance(m, Metric)
        self.assertDictEqual({}, m.tags)
        self.assertEqual(None, m.description)

    def test_series(self):
        # Insert series.
        series = Series(ENTITY, NAME)
        series.add_samples(Sample(1, datetime.now()))
        series_service = SeriesService(self.connection)
        series_service.insert(series)

        time.sleep(self.wait_time)

        result = self.service.series(metric=NAME, min_insert_date='current_hour')
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        series = result[0]
        self.assertIsNotNone(series)
        self.assertIsInstance(series, Series)
        self.assertEqual(NAME, series.metric)
        self.assertEqual(ENTITY, series.entity)
        self.assertEqual({}, series.tags)

    def common_checks(self, metric):
        self.assertEqual(NAME, metric.name)
        self.assertTrue(metric.enabled)
        self.assertEqual(DATA_TYPE, metric.data_type)
        self.assertEqual(PERSISTENT, metric.persistent)
        self.assertEqual(FILTER, metric.filter)
        self.assertEqual(MIN_VALUE, metric.min_value)
        self.assertEqual(MAX_VALUE, metric.max_value)
        self.assertEqual(INVALID_ACTION, metric.invalid_action)
        self.assertEqual(DESCRIPTION, metric.description)
        self.assertEqual(RETENTION_DAYS, metric.retention_days)
        self.assertEqual(SERIES_RETENTION_DAYS, metric.series_retention_days)
        self.assertFalse(metric.versioned)
        self.assertEqual(INTERPOLATE, metric.interpolate)
        self.assertEqual(UNITS, metric.units)
        self.assertEqual(TIME_ZONE, metric.time_zone)
        self.assertTrue(isinstance(metric.created_date, datetime))

    @classmethod
    def tearDownClass(cls):
        """
        Clean up ATSD.
        """
        cls.service.delete(NAME)
        super().tearDownClass()