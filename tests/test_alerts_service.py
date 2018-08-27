# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
import time
from atsd_client.models import Alert, AlertsQuery, AlertHistoryQuery, EntityFilter, DateFilter, Series, Sample
from service_test_base import ServiceTestBase, SeriesService

ENTITY = 'pyapi.alerts_service.entity'
METRIC = 'test_alert_metric_1'
RULE = 'test_rule_1'
ID = 1
ACKNOWLEDGED = False
VALUE = 1
MESSAGE = ''
TAGS = {}
TEXT_VALUE = '1'
SEVERITY = 'WARNING'
REPEAT_COUNT = 0
OPEN_VALUE = 1
INTERVAL = {"count": 2, "unit": "MINUTE"}
START_DATE = datetime.now()
ef = EntityFilter(entity=ENTITY)
df = DateFilter(start_date=START_DATE, interval=INTERVAL)


class TestAlertsService(ServiceTestBase):

    def setUp(self):
        """
        Insert series to open the alert.
        """
        series = Series(ENTITY, METRIC)
        series.add_samples(Sample(VALUE, datetime.now()))
        self._series_service = SeriesService(self.connection)
        self._series_service.insert(series)
        time.sleep(self.wait_time)

    def test_fields_match(self):
        """
        Check fields of Alert model were set as expected.
        """
        LAST_EVENT_DATE = datetime.now()
        OPEN_DATE = LAST_EVENT_DATE
        a = Alert(ID, RULE, ENTITY, METRIC, LAST_EVENT_DATE, OPEN_DATE, VALUE, MESSAGE, TAGS, TEXT_VALUE, SEVERITY,
                  REPEAT_COUNT, ACKNOWLEDGED, OPEN_VALUE)
        self.assertEqual(ID, a.id)
        self.assertEqual(MESSAGE, a.message)
        self.common_checks(a)

    def test_query(self):
        rules = [RULE]
        query = AlertsQuery(entity_filter=ef, date_filter=df, rules=rules)
        result = self.service.query(query)
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        a = result[0]
        self.common_checks(a)

    def test_update(self):
        query = AlertsQuery(entity_filter=ef, date_filter=df, rules=[RULE])
        result = self.service.query(query)
        ID = result[0].id
        global ACKNOWLEDGED
        ACKNOWLEDGED = True
        alert_dict = {"id": ID, "acknowledged": ACKNOWLEDGED}
        self.service.update(alert_dict)

        time.sleep(self.wait_time)

        query = AlertsQuery(entity_filter=ef, date_filter=df, acknowledged=ACKNOWLEDGED)
        result = self.service.query(query)
        # print(result)
        self.assertIsNotNone(result)
        self.assertEqual(1, len(result))
        a = result[0]
        self.assertEqual(ID, a.id)
        self.common_checks(a)

    @unittest.skip("Expected behavior is unknown")
    def test_history_query(self):
        # Insert series to close the alert.
        series = Series(ENTITY, METRIC)
        series.add_samples(Sample(-1, datetime.now()))
        self._series_service.insert(series)

        time.sleep(self.wait_time)

        query = AlertHistoryQuery(entity_filter=ef, date_filter=df, rule=RULE, metric=METRIC)
        result = self.service.history_query(query)
        # print(result)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        a = result[0]
        self.common_checks(a)

    def tearDown(self):
        # Insert series to close the alert.
        series = Series(ENTITY, METRIC)
        series.add_samples(Sample(-1, datetime.now()))
        self._series_service.insert(series)
        time.sleep(self.wait_time)

    def common_checks(self, alert):
        self.assertEqual(RULE, alert.rule)
        self.assertEqual(ENTITY, alert.entity)
        self.assertEqual(METRIC, alert.metric)
        self.assertTrue(isinstance(alert.last_event_date, datetime))
        self.assertTrue(isinstance(alert.open_date, datetime))
        self.assertEqual(VALUE, alert.value)
        self.assertEqual(TAGS, alert.tags)
        self.assertEqual(TEXT_VALUE, alert.text_value)
        self.assertEqual(SEVERITY, alert.severity)
        self.assertEqual(REPEAT_COUNT, alert.repeat_count)
        self.assertEqual(ACKNOWLEDGED, alert.acknowledged)
        self.assertEqual(OPEN_VALUE, alert.open_value)
