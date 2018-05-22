# -*- coding: utf-8 -*-

import logging
import unittest
import time

from datetime import datetime

import atsd_client
from atsd_client import services
from atsd_client.models import EntityFilter, DateFilter
from atsd_client.models import Message
from atsd_client.models import MessageQuery
from atsd_client import _time_utilities as tu

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.entity'
TYPE = 'pyapi.type'
SOURCE = 'pyapi.source'
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
SEVERITY = 'MINOR'
MESSAGE = 'pyapi test message'


def get_connection():
    conn = atsd_client.connect_url('https://localhost:8443', 'axibase', 'axibase')
    return conn


class TestMessageService(unittest.TestCase):
    def setUp(self):
        self.ms = services.MessageService(
            get_connection()
        )

    """
    Check parameters were set as expected.
    """

    def test_fields_match(self):
        DATE = datetime.now()
        m = Message(TYPE, SOURCE, ENTITY, DATE, SEVERITY, TAGS, MESSAGE, persist=False)
        self.assertEqual(TYPE, m.type)
        self.assertEqual(SOURCE, m.source)
        self.assertEqual(ENTITY, m.entity)
        self.assertEqual(tu.to_date(DATE), m.date)
        self.assertEqual(SEVERITY, m.severity)
        self.assertEqual(TAGS, m.tags)
        self.assertEqual(MESSAGE, m.message)
        self.assertFalse(m.persist)

    """
    Check inserted and retrieved messages are equal.
    """

    def test_insert_retrieve(self):
        DATE = datetime.now()
        msg = Message(TYPE, SOURCE, ENTITY, DATE, SEVERITY, TAGS, MESSAGE)
        self.ms.insert(msg)

        time.sleep(2)

        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date=DATE, end_date=datetime.now())
        query = MessageQuery(entity_filter=ef, date_filter=df)
        result = self.ms.query(query)

        print(result)

        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        m = result[0]
        self.assertIsInstance(m, Message)
        """
        In the future may be replaced with:
        self.assertItemsEqual(msg.__dict__.items(), m.__dict__.items())
        """
        self.assertEqual(msg.type, m.type)
        self.assertEqual(msg.source, m.source)
        self.assertEqual(msg.entity, m.entity)
        # Uncomment when JodaTime will be replaced
        # self.assertEqual(msg.date, m.date)
        self.assertEqual(msg.severity, m.severity)
        self.assertEqual(msg.tags, m.tags)
        self.assertEqual(msg.message, m.message)
        self.assertEqual(msg.persist, m.persist)
