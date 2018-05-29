# -*- coding: utf-8 -*-

import logging
import time

from datetime import datetime

from atsd_client import services
from atsd_client.models import EntityFilter, DateFilter
from atsd_client.models import Property
from atsd_client.models import PropertiesQuery
from atsd_client import _time_utilities as tu

from service_test_base import ServiceTestBase

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.entity'
TYPE = 'pyapi.type'
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
KEY_NAME = 'pyapi.key'
KEY_VALUE = 'pyapi.key-value'
KEY = {KEY_NAME: KEY_VALUE}


class TestPropertiesService(ServiceTestBase):

    def setUp(self):
        self.ps = services.PropertiesService(self.connection())

    """
    Check parameters were set as expected.
    """

    def test_fields_match(self):
        DATE = datetime.now()
        p = Property(TYPE, ENTITY, TAGS, KEY, DATE)
        self.assertEqual(TYPE, p.type)
        self.assertEqual(ENTITY, p.entity)
        self.assertEqual(TAGS, p.tags)
        self.assertEqual(KEY, p.key)
        self.assertEqual(tu.to_date(DATE), p.date)

    """
    Check inserted and retrieved properties are equal.
    """

    def test_insert_retrieve(self):
        DATE = datetime.now()
        prop = Property(TYPE, ENTITY, TAGS, KEY, DATE)
        self.ps.insert(prop)

        time.sleep(2)

        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(start_date=DATE, end_date=datetime.now())
        query = PropertiesQuery(type=TYPE, entity_filter=ef, date_filter=df)
        result = self.ps.query(query)

        # print(result)

        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        p = result[0]
        """
        In the future may be replaced with:
        self.assertItemsEqual(prop.__dict__.items(), p.__dict__.items())
        """
        self.assertIsInstance(p, Property)
        self.assertEqual(prop.type, p.type)
        self.assertEqual(prop.entity, p.entity)
        # Uncomment when JodaTime will be replaced
        # self.assertEqual(prop.date, p.date)
        self.assertEqual(prop.key, p.key)
        self.assertEqual(prop.tags, p.tags)
