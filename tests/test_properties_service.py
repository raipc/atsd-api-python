# -*- coding: utf-8 -*-

import time
from datetime import datetime
from atsd_client.models import EntityFilter, DateFilter
from atsd_client.models import Property
from atsd_client.models import PropertiesQuery
from service_test_base import ServiceTestBase


ENTITY = 'pyapi.properties_service.entity'
TYPE = 'pyapi.type'
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
TAGS = {TAG: TAG_VALUE}
KEY_NAME = 'pyapi.key'
KEY_VALUE = 'pyapi.key-value'
KEY = {KEY_NAME: KEY_VALUE}
DATE = datetime.now()
INTERVAL = {"count": 5, "unit": "MINUTE"}
ef = EntityFilter(entity=ENTITY)
df = DateFilter(start_date=DATE, interval=INTERVAL)


class TestPropertiesService(ServiceTestBase):

    @classmethod
    def setUpClass(cls):
        """
        Insert property.
        """
        super().setUpClass()
        prop = Property(TYPE, ENTITY, TAGS, KEY, DATE)
        cls.service.insert(prop)
        time.sleep(cls.wait_time)

    def test_fields_match(self):
        """
        Check fields of Property model were set as expected.
        """
        DATE = datetime.now()
        p = Property(TYPE, ENTITY, TAGS, KEY, DATE)
        self.common_checks(p)

    def test_retrieve(self):
        """
        Check inserted and retrieved properties are equal.
        """
        query = PropertiesQuery(type=TYPE, entity_filter=ef, date_filter=df)
        result = self.service.query(query)
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        p = result[0]
        self.common_checks(p)

    def test_type_query(self):
        result = self.service.type_query(ENTITY)
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        p = result[0]
        self.assertEqual(TYPE, p)

    def common_checks(self, prop):
        self.assertEqual(TYPE, prop.type)
        self.assertEqual(ENTITY, prop.entity)
        self.assertEqual(TAGS, prop.tags)
        self.assertEqual(KEY, prop.key)
        self.assertTrue(isinstance(prop.date, datetime))