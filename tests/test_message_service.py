# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime
from atsd_client.models import EntityFilter, DateFilter
from atsd_client.models import Message
from atsd_client.models import MessageQuery
from service_test_base import ServiceTestBase

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.message_service.entity'
TYPE = 'pyapi.type'
SOURCE = 'pyapi.source'
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
SEVERITY = 'MINOR'
MESSAGE_1 = 'pyapi test message'
MESSAGE_2 = 'pyapi test message expression'
DATE = datetime.now()
INTERVAL = {"count": 5, "unit": "MINUTE"}
ef = EntityFilter(entity=ENTITY)
df = DateFilter(start_date=DATE, interval=INTERVAL)


class TestMessageService(ServiceTestBase):

    @classmethod
    def setUpClass(cls):
        """
        Insert messages.
        """
        super().setUpClass()
        msg_1 = Message(TYPE, SOURCE, ENTITY, DATE, SEVERITY, TAGS, MESSAGE_1)
        msg_2 = Message(TYPE, SOURCE, ENTITY, DATE, SEVERITY, TAGS, MESSAGE_2)
        cls.service.insert(msg_1)
        cls.service.insert(msg_2)
        time.sleep(cls.wait_time)

    def test_fields_match(self):
        """
        Check fields of Message model were set as expected.
        """
        m = Message(TYPE, SOURCE, ENTITY, DATE, SEVERITY, TAGS, MESSAGE_1)
        self.assertEqual(MESSAGE_1, m.message)
        self.common_checks(m)

    def test_retrieve(self):
        """
        Check inserted and retrieved messages are equal.
        """
        query = MessageQuery(entity_filter=ef, date_filter=df)
        result = self.service.query(query)
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        m = result[0]
        self.assertIsInstance(m, Message)
        self.common_checks(m)

    def test_query_expr(self):
        """
        Check query method with expression field.
        """
        exp = "message LIKE '* expression'"
        query = MessageQuery(entity_filter=ef, date_filter=df, expression=exp)
        result = self.service.query(query)
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        m = result[0]
        self.assertEqual(MESSAGE_2, m.message)
        self.common_checks(m)

    def common_checks(self, message):
        self.assertEqual(TYPE, message.type)
        self.assertEqual(SOURCE, message.source)
        self.assertEqual(ENTITY, message.entity)
        self.assertTrue(isinstance(message.date, datetime))
        self.assertEqual(SEVERITY, message.severity)
        self.assertEqual(TAGS, message.tags)
        self.assertTrue(message.persist)
