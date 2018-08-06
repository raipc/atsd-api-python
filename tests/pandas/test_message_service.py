# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime
from atsd_client.models import EntityFilter, DateFilter
from atsd_client.models import Message
from atsd_client.models import MessageQuery
from tests import service_test_base

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.message_service_df.entity'
TYPE = 'pyapi.type_df'
SOURCE = 'pyapi.source_df'
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
SEVERITY = 'MINOR'
MESSAGE = 'pyapi test message DataFrame'
DATE = datetime.now()
INTERVAL = {"count": 5, "unit": "MINUTE"}


class TestMessageService(service_test_base.ServiceTestBase):

    def setUp(self):
        """
        Insert message.
        """
        msg = Message(TYPE, SOURCE, ENTITY, DATE, SEVERITY, TAGS, MESSAGE)
        self.service.insert(msg)
        time.sleep(self.wait_time)

    def test_query_dataframe(self):
        exp = "message LIKE '* DataFrame'"
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(interval=INTERVAL, end_date=datetime.now())
        query = MessageQuery(entity_filter=ef, date_filter=df, expression=exp)
        result = self.service.query_dataframe(query)
        # print(result)
        self.assertIsNotNone(result)
        self.assertEqual((1, 7), result.shape)
        self.assertTrue(isinstance(result.loc[0, 'date'], datetime))
        self.assertEqual(MESSAGE, result.loc[0, 'message'])
        self.assertEqual(TYPE, result.loc[0, 'type'])
        self.assertEqual(SOURCE, result.loc[0, 'source'])
        self.assertEqual(ENTITY, result.loc[0, 'entity'])
        self.assertEqual(SEVERITY, result.loc[0, 'severity'])
        self.assertEqual(TAG_VALUE, result.loc[0, TAG])
