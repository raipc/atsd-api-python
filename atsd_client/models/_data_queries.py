"""
Copyright 2015 Axibase Corporation or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

https://www.axibase.com/atsd/axibase-apache-2.0.pdf

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""


import numbers

from ._data_models import Property
from ._data_models import _Model
from ._data_models import Alert


class SeriesType(object):
    HISTORY = 'HISTORY'
    FORECAST = 'FORECAST'
    FORECAST_DEVIATION = 'FORECAST_DEVIATION'


class Interpolate(object):
    NONE = 'NONE'
    LINEAR = 'LINEAR'
    STEP = 'STEP'


class TimeUnit(object):
    MILLISECOND = 'MILLISECOND'
    SECOND = 'SECOND'
    MINUTE = 'MINUTE'
    HOUR = 'HOUR'
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    QUARTER = 'QUARTER'
    YEAR = 'YEAR'


class AggregateType(object):
    DETAIL = 'DETAIL'
    COUNT = 'COUNT'
    MIN = 'MIN'
    MAX = 'MAX'
    AVG = 'AVG'
    SUM = 'SUM'
    PERCENTILE_999 = 'PERCENTILE_999'
    PERCENTILE_995 = 'PERCENTILE_995'
    PERCENTILE_99 = 'PERCENTILE_99'
    PERCENTILE_95 = 'PERCENTILE_95'
    PERCENTILE_90 = 'PERCENTILE_90'
    PERCENTILE_75 = 'PERCENTILE_75'
    PERCENTILE_50 = 'PERCENTILE_50'
    STANDARD_DEVIATION = 'STANDARD_DEVIATION'
    FIRST = 'FIRST'
    LAST = 'LAST'
    DELTA = 'DELTA'
    WAVG = 'WAVG'
    WTAVG = 'WTAVG'
    THRESHOLD_COUNT = 'THRESHOLD_COUNT'
    THRESHOLD_DURATION = 'THRESHOLD_DURATION'
    THRESHOLD_PERCENT = 'THRESHOLD_PERCENT'


class _Rate(_Model):
    _required_props = ()
    _allowed_props = ('interval', 'counter')

    def __init__(self, interval=None, counter=None):
        self.interval = interval
        self.counter = counter

    def set_interval(self, count, unit=TimeUnit.SECOND):
        """
        :param count: number
        :param unit: use :class:`.TimeUnit` enum, default TimeUnit.SECOND
        """
        if not isinstance(count, numbers.Number):
            raise ValueError('interval count expected number, found: '
                             + str(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong interval unit')
        self.interval = {'count': count, 'unit': unit}


class _Group(_Model):
    """
    represents aggregate param group
    """
    _required_props = ('type',)
    _allowed_props = ('interpolate', 'truncate', 'interval')

    def __init__(self, type, interpolate=None, truncate=None, interval=None):
        self.type = type

        self.interpolate = interpolate
        self.truncate = truncate
        self.interval = interval

    def set_interval(self, count, unit=TimeUnit.SECOND):
        """
        :param count: number
        :param unit: use :class:`.TimeUnit` enum, default TimeUnit.SECOND
        """
        if not isinstance(count, numbers.Number):
            raise ValueError('interval count expected number, found: '
                             + str(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong interval unit')
        self.interval = {'count': count, 'unit': unit}


class _Aggregator(_Model):
    """
    represents aggregate param of :class:`.SeriesQuery`
    """
    _required_props = ('types', 'interval')
    _allowed_props = ('interpolate',
                      'threshold',
                      'calendar',
                      'workingMinutes',
                      'counter')

    def __init__(self, types, interval,
                 interpolate=None,
                 threshold=None,
                 calendar=None,
                 workingMinutes=None,
                 counter=None):

        self.interval = interval
        self.types = types

        self.interpolate = interpolate
        self.threshold = threshold
        self.calendar = calendar
        self.workingMinutes = workingMinutes
        self.counter = counter

    def set_types(self, *types):
        """specified aggregation types

        :param types: use :class:`.AggregateType` enum objects
        """
        self.types = []
        for typ in types:
            if not hasattr(AggregateType, typ):
                raise ValueError('wrong aggregate type')
            self.types.append(typ)

    def set_interval(self, count, unit=TimeUnit.SECOND):
        """
        :param count: number
        :param unit: use :class:`.TimeUnit` enum, default TimeUnit.SECOND
        """
        if not isinstance(count, numbers.Number):
            raise ValueError('interval count expected number, found: '
                             + str(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong interval unit')
        self.interval = {'count': count, 'unit': unit}

    def set_thresholds(self, min, max):
        self.threshold = {'min': min, 'max': max}

    def set_workingMinutes(self, start, end):
        self.workingMinutes = {'start': start, 'end': end}

    def set_calendar(self, name):
        self.calendar = {'name': name}


class SeriesQuery(_Model):
    _allowed_props = ('startTime',
                      'endTime',
                      'limit',
                      'last',
                      'tags',
                      'type',
                      'group',
                      'rate',
                      'aggregate',
                      'requestId')
    _required_props = ('entity', 'metric')

    def rate(self, interval=None, counter=None):
        """add empty rate property to series query

        :return: :class:`._Rate` object

        Usage::

            >>>query = SeriesQuery(ENTITY, METRIC)
            >>>rate = query.rate()
            >>>rate.counter = False
            >>>series = svc.retrieve_series(query)

        """
        self._rate = _Rate(interval, counter)
        return self._rate

    def aggregate(self, types=None, interval=None,
                  interpolate=None,
                  threshold=None,
                  calendar=None,
                  workingMinutes=None,
                  counter=None):
        """add aggregate property to series query
        by default types = [AggregateType.DETAIL], interval = 1 sec

        :return: :class:`._Aggregator` object

        Usage::

            >>>query = SeriesQuery(ENTITY, METRIC)
            >>>aggr = query.aggregate()
            >>>aggr.set_interval(10, TimeUnit.DAY)
            >>>aggr.set_types(AggregateType.MAX, AggregateType.MIN)
            >>>series = svc.retrieve_series(query)

        """
        if types is None:
            types = [AggregateType.DETAIL]
        if interval is None:
            interval = {'count': 1, 'unit': TimeUnit.SECOND}

        self._aggregate = _Aggregator(types, interval,
                                      interpolate,
                                      threshold,
                                      calendar,
                                      workingMinutes,
                                      counter)
        return self._aggregate

    def group(self, type, interpolate=None, truncate=None, interval=None):
        """add group property to series query

        :param type: :class:`.AggregateType` enum
        :return: :class:`._Group` object

        Usage::

            >>>query = SeriesQuery(ENTITY, METRIC)
            >>>group = query.group(AggregateType.COUNT)
            >>>group.set_interval(1, TimeUnit.SECOND)
            >>>series = svc.retrieve_series(query)

        """
        self._group = _Group(type, interpolate, truncate, interval)
        return self._group

    def __init__(self, entity, metric,
                 startTime=None,
                 endTime=None,
                 limit=None,
                 last=None,
                 tags=None,
                 type=None,
                 group=None,
                 rate=None,
                 aggregate=None,
                 requestId=None):
        """
        :param entity: str entity name
        :param metric: str metric name
        :param group: use group() method to set property
        :param rate: use rate() method to set property
        :param aggregate: use aggregate() method to set property
        """
        self.entity = entity
        self.metric = metric

        self.startTime = startTime
        self.endTime = endTime
        self.limit = limit
        self.last = last
        self.tags = tags
        self.type = type
        self._group = group
        self._rate = rate
        self._aggregate = aggregate
        self.requestId = requestId


class AlertsQuery(_Model):
    _allowed_props = ('metrics',
                      'entities',
                      'rules',
                      'severities',
                      'minSeverity')
    _required_props = ()

    def __init__(self,
                 metrics=None,
                 entities=None,
                 rules=None,
                 severities=None,
                 minSeverity=None):
        self.metrics = metrics
        self.entities = entities
        self.rules = rules
        self.severities = severities
        self.minSeverity = minSeverity


class PropertiesQuery(_Model):
    _allowed_props = ('startTime',
                      'endTime',
                      'limit',
                      'key',
                      'keyExpression')
    _required_props = ('entity', 'type')

    def __init__(self, type, entity,
                 startTime=None,
                 endTime=None,
                 limit=None,
                 key=None,
                 keyExpression=None):
        """
        :param type: str
        :param entity: str
        """
        self.entity = entity
        self.type = type

        self.startTime = startTime
        self.endTime = endTime
        self.limit = limit
        self.key = key
        self.keyExpression = keyExpression


class PropertiesMatcher(_Model):
    _allowed_props = ('entity', 'key', 'createdBeforeTime')
    _required_props = ('type',)

    def __init__(self, type,
                 entity=None,
                 key=None,
                 createdBeforeTime=None):
        """
        :param type: str
        """
        self.type = type

        self.entity = entity
        self.key = key
        self.createdBeforeTime = createdBeforeTime

class AlertHistoryQuery(_Model):
    _allowed_props = ('entityGroup', 'limit')
    _required_props = ('entity', 'metric', 'startTime', 'endTime', 'rule')

    def __init__(self, entity, metric, startTime, endTime, rule,
                 entityGroup=None,
                 limit=None):
        """
        :param entity: str
        :param metric: str
        :param startTime: long int
        :param endTime: long int
        :param rule: str
        """
        self.entity = entity
        self.metric = metric
        self.startTime = startTime
        self.endTime = endTime
        self.rule = rule

        self.entityGroup = entityGroup
        self.limit = limit


class BatchPropertyCommand(object):
    def __init__(self, action, properties=None, matchers=None):
        self.action = action
        if properties:
            if len(properties) is 0:
                self.empty = True
            self.properties = properties
            self._properties_data = [p._serialize() for p in properties]
        else:
            if len(matchers) is 0:
                self.empty = True
            self.matchers = matchers
            self._matchers_data = [m._serialize() for m in matchers]
        self.empty = False

    def _serialize(self):
        data = {'action': self.action}
        try:
            data['properties'] = self._properties_data
        except AttributeError:
            data['matchers'] = self._matchers_data

        return data

    @staticmethod
    def create_insert_command(*insertions):
        """
        :param insertions: :class:`.Property` objects
        :return: :class:`BatchPropertyCommand` instance
        """
        for insertion in insertions:
            if not isinstance(insertion, Property):
                raise TypeError('expected:' + repr(Property)
                                + ', found:' + repr(type(insertion)))

        return BatchPropertyCommand('insert', properties=insertions)

    @staticmethod
    def create_delete_command(type, entity, key=None):
        """
        :param type: `str`
        :param entity: `str`
        :param key: `dict`
        :return: :class:`BatchPropertyCommand` instance
        """
        prop = Property(type, entity, {})
        if key is not None:
            prop.key = key
        return BatchPropertyCommand('delete', properties=(prop,))

    @staticmethod
    def create_delete_match_command(*matchers):
        """
        :param matchers: :class:`.PropertiesMatcher` objects
        :return: command instance
        """
        for matcher in matchers:
            if not isinstance(matcher, PropertiesMatcher):
                raise TypeError('expected:' + repr(PropertiesMatcher)
                                + ', found:' + repr(type(matcher)))

        return BatchPropertyCommand('delete-match', matchers=matchers)


class BatchAlertCommand(object):
    def __init__(self, action, alerts, fields=None):
        if len(alerts) is 0:
            self.empty = True
            return

        self.empty = False
        self.action = action
        self.alerts = alerts
        self.fields = fields
        self._data_alerts = [alert._serialize() for alert in alerts]

    def _serialize(self):
        return {
            'action': self.action,
            'alerts': self._data_alerts,
            'fields': self.fields
        }

    @staticmethod
    def create_delete_command(*alert_ids):
        """
        :param alert_ids: str
        :return: :class:`.BatchAlertCommand` instance
        """
        return BatchAlertCommand('delete',
                                 alerts=[Alert(i) for i in alert_ids])

    @staticmethod
    def create_update_command(acknowledge, *alert_ids):
        """
        :param alert_ids: str
        :return: :class:`.BatchAlertCommand` instance
        """
        return BatchAlertCommand('update',
                                 alerts=[Alert(id) for id in alert_ids],
                                 fields={'acknowledge': acknowledge})