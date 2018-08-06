# -*- coding: utf-8 -*-

import logging
from datetime import datetime
import time

from atsd_client.services import SeriesService
from tests import service_test_base
from atsd_client.models import Series, Sample

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.sql_service_df.entity'
METRIC = 'pyapi.sql_service_df.metric'
VALUE = 1
QUERY = 'SELECT * FROM "{}"'.format(METRIC)


class TestSQLService(service_test_base.ServiceTestBase):

    def setUp(self):
        """
        Insert series.
        """
        series = Series(ENTITY, METRIC)
        series.add_samples(Sample(VALUE, datetime.now()))
        self._series_service = SeriesService(self.connection)
        self._series_service.insert(series)
        time.sleep(self.wait_time)

    def test_query(self):
        result = self.service.query(QUERY)
        # print(result)
        self.assertIsNotNone(result)
        self.assertEqual((1, 7), result.shape)
        self.assertTrue(isinstance(result.at[0, 'datetime'], str))
        self.assertEqual(METRIC, result.at[0, 'metric'])
        self.assertEqual(ENTITY, result.at[0, 'entity'])
        self.assertEqual(VALUE, result.at[0, 'value'])