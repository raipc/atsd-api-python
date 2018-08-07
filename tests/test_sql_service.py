# -*- coding: utf-8 -*-
from datetime import datetime
import time
from service_test_base import ServiceTestBase, SeriesService
from atsd_client.models import Series, Sample

ENTITY = 'pyapi.sql_service.entity'
METRIC = 'pyapi.sql_service.metric'
VALUE = 1
QUERY = 'SELECT * FROM "{}"'.format(METRIC)


class TestSQLService(ServiceTestBase):

    def setUp(self):
        """
        Insert series.
        """
        series = Series(ENTITY, METRIC)
        series.add_samples(Sample(VALUE, datetime.now()))
        self._series_service = SeriesService(self.connection)
        self._series_service.insert(series)
        time.sleep(self.wait_time)

    def test_query_with_params(self):
        params = {'outputFormat': 'json'}
        response = self.service.query_with_params(QUERY, params)
        # print(response)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(1, len(response["data"]))
        value = response["data"][0][2]
        metric = response["data"][0][4]
        entity = response["data"][0][5]
        self.assertEqual(VALUE, value)
        self.assertEqual(METRIC, metric)
        self.assertEqual(ENTITY, entity)
