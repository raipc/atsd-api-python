# -*- coding: utf-8 -*-


import logging
import random
import unittest

import sys
import time
from datetime import datetime
from datetime import timedelta

import atsd_client
from atsd_client import models
from atsd_client import services
from atsd_client.exceptions import DataParseException
from atsd_client.models import AggregateType, SeriesFilter, EntityFilter, DateFilter, VersioningFilter, Aggregate, \
    TransformationFilter, Group, Rate
from atsd_client.models import Series
from atsd_client.models import SeriesQuery
from atsd_client.models import TimeUnit, Sample

logger = logging.getLogger()
logger.disabled = True

ENTITY = 'pyapi.entity'
METRIC = 'pyapi.metric'
TAG = 'pyapi.tag'
TAG_VALUE = 'pyapi.tag-value'
WAIT_TIME = 4
TEST_NAME = 'pyapi/test'
GROUP_NAME = TEST_NAME
VALUE = 33333
VERSION_METRIC = 'pyapi.versioning.metric'


def get_timestamp():
    return int(time.time() * 1000)


def get_connection():
    conn = atsd_client.connect_url('https://atsd_hostname:8443', 'user', 'password')
    return conn


def insert_series_sample(data_service, val=None, *vals):
    if val is None:
        val = random.randint(0, VALUE - 1)

    series = Series(ENTITY, METRIC)
    series.tags = {TAG: TAG_VALUE}
    series.add_samples(Sample(val, get_timestamp()))
    if vals:
        for i, v in enumerate(vals):
            series.add_samples(Sample(v, get_timestamp() + i + 1))

    print('insertion =', series)

    return data_service.insert(series)


class TestSeriesService(unittest.TestCase):
    def setUp(self):
        self.svc = services.SeriesService(
            get_connection()
        )

    def test_insert_retrieve_series(self):
        val = random.randint(0, VALUE - 1)

        insert_series_sample(self.svc, val)
        time.sleep(WAIT_TIME + 2)

        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]})
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(startDate=now - timedelta(hours=1), endDate=now)
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)

        series = self.svc.query(query)
        for s in series:
            print(s)

        self.assertIsNotNone(series)
        self.assertGreater(len(series), 0)

        s = series[0]
        self.assertIsInstance(s, Series)

        self.assertGreater(len(s.data), 0)
        self.assertEqual(s.get_last_value(), val)

    def test_aggregate_series(self):
        val = random.randint(0, VALUE - 1)

        insert_series_sample(self.svc, val, val + 1)
        time.sleep(WAIT_TIME)

        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]})
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(startDate=now - timedelta(hours=1), endDate=now)
        aggr = Aggregate(period={'count': 10, 'unit': TimeUnit.SECOND}, types=[AggregateType.MAX, AggregateType.MIN])
        tf = TransformationFilter(aggregate=aggr)
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, transformation_filter=tf)

        series = self.svc.query(query)
        self.assertEqual(len(series), 2)

        if series[0].aggregate['type'] == 'MAX':
            max = series[0].get_last_value()
            min = series[1].get_last_value()
        else:
            min = series[0].get_last_value()
            max = series[1].get_last_value()

        self.assertGreaterEqual(max, min)

    def test_insert_retrieve_versioning(self):

        test_status = 'pyapi.status'
        now = datetime.now()

        series = Series(ENTITY, VERSION_METRIC)
        val = random.randint(0, VALUE - 1)
        series.add_samples(Sample(value=val, time=now - timedelta(seconds=2), version={'status': test_status}))

        sf = SeriesFilter(metric=VERSION_METRIC)
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(startDate=now - timedelta(hours=1), endDate=now)
        vf = VersioningFilter(versioned=True)
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, versioning_filter=vf)

        successful = self.svc.insert(series)
        time.sleep(WAIT_TIME)
        series, = self.svc.query(query)
        print(series)
        last_sample = series.data[-1]

        self.assertTrue(successful)
        self.assertEquals(last_sample.v, val)
        self.assertIsNotNone(last_sample.version)
        self.assertEquals(last_sample.version['status'], test_status)

    def test_series_data_field_empty(self):
        series = Series(entity=ENTITY,
                        metric=METRIC)
        series.tags = {TAG: TAG_VALUE}
        print(series)

        with self.assertRaises(DataParseException) as cm:
            self.svc.insert(series)

        self.assertEqual(cm.exception.non_parsed_field, 'data')

    def test_forecast(self):
        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]}, type=models.SeriesType.FORECAST)
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(startDate=now - timedelta(hours=1), endDate=now)
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df)

        series = self.svc.query(query)
        self.assertEqual(series[0].type, models.SeriesType.FORECAST)

    def test_rate(self):
        v1 = 5
        v2 = 3
        insert_series_sample(self.svc, v1, v2)
        time.sleep(WAIT_TIME + 2)

        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]})
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(startDate=now - timedelta(hours=1), endDate=now)
        tf = TransformationFilter(rate=Rate(counter=False))
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, transformation_filter=tf)

        series = self.svc.query(query)
        self.assertEqual(int(series[0].get_last_value()), v2 - v1)

    def test_group(self):
        time.sleep(1)
        insert_series_sample(self.svc, VALUE - 1)
        time.sleep(WAIT_TIME)

        now = datetime.now()
        sf = SeriesFilter(metric=METRIC, tags={TAG: [TAG_VALUE]})
        ef = EntityFilter(entity=ENTITY)
        df = DateFilter(startDate=now - timedelta(hours=1), endDate=now)
        tf = TransformationFilter(group=Group(type=AggregateType.COUNT, period={'count': 1, 'unit': TimeUnit.SECOND}))
        query = SeriesQuery(series_filter=sf, entity_filter=ef, date_filter=df, transformation_filter=tf)

        series = self.svc.query(query)
        self.assertEqual(series[0].get_last_value(), 1)


if __name__ == '__main__':
    print('python version: ', sys.version, '\n')
    unittest.main()
