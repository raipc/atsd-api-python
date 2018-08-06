# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime
from atsd_client.models import EntityFilter, DateFilter
from atsd_client.models import Property
from atsd_client.models import PropertiesQuery
from tests import service_test_base
logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.properties_service_df.entity'
TYPE = 'pyapi.type_df'
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
KEY_NAME = 'pyapi.key'
KEY_VALUE = 'pyapi.key-value'
KEY = {KEY_NAME: KEY_VALUE}
DATE = datetime.now()


class TestPropertiesService(service_test_base.ServiceTestBase):

    def setUp(self):
        """
        Insert property.
        """
        super().setUpClass()
        prop = Property(TYPE, ENTITY, TAGS, KEY, datetime.now())
        self.service.insert(prop)
        time.sleep(self.wait_time)

    def test_query_dataframe(self):
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date=DATE, end_date=datetime.now())
        query = PropertiesQuery(type=TYPE, entity_filter=ef, date_filter=df)
        result = self.service.query_dataframe(query)
        # print(result)
        self.assertIsNotNone(result)
        self.assertEqual((1, 5), result.shape)
        self.assertTrue(isinstance(result.loc[0, 'date'], datetime))
        self.assertEqual(KEY_VALUE, result.loc[0, KEY_NAME])
        self.assertEqual(TYPE, result.loc[0, 'type'])
        self.assertEqual(TAG_VALUE, result.loc[0, TAG])
        self.assertEqual(ENTITY, result.loc[0, 'entity'])
