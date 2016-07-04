# -*- coding: utf-8 -*-

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
from datetime import datetime
from ..utilities import copy_not_empty_attrs

from ._data_models import Property
from ._data_models import to_posix_timestamp
from .._jsonutil import Serializable
from ._data_models import Alert

try:
    unicode = unicode
except NameError:
    unicode = str


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


class Severity(object):
    UNDEFINED = 0
    UNKNOWN = 1
    NORMAL = 2
    WARNING = 3
    MINOR = 4
    MAJOR = 5
    CRITICAL = 6
    FATAL = 7


class Rate(Serializable):
    def __init__(self, period=None, counter=None):

        #: `dict` {'count': `Number`, 'unit': :class:`.TimeUnit`},
        #: use ``set_period`` method instead setting explicitly
        self.period = period
        #: `bool`
        self.counter = counter

    def set_period(self, count, unit=TimeUnit.SECOND):
        """
        :param count: number
        :param unit: use :class:`.TimeUnit` enum, default TimeUnit.SECOND
        """
        if not isinstance(count, numbers.Number):
            raise ValueError('period count expected number, found: '
                             + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong period unit')
        self.period = {'count': count, 'unit': unit}


class Group(Serializable):
    """
    represents aggregate param group
    """
    def __init__(self, type, interpolate=None, truncate=None, period=None):
        #: :class:`.AggregateType`
        self.type = type

        #: :class:`.Interpolate`
        self.interpolate = interpolate
        #: `bool` default False
        self.truncate = truncate
        #: `dict` {'count': `Number`, 'unit': :class:`.TimeUnit`},
        #: use ``set_period`` method instead setting explicitly
        self.period = period

    def set_period(self, count, unit=TimeUnit.SECOND):
        """
        :param count: number
        :param unit: use :class:`.TimeUnit` enum, default TimeUnit.SECOND
        """
        if not isinstance(count, numbers.Number):
            raise ValueError('period count expected number, found: '
                             + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong period unit')
        self.period = {'count': count, 'unit': unit}


class Aggregator(Serializable):
    """
    represents aggregate param of :class:`.SeriesQuery`
    """
    def __init__(self, types, period,
                 interpolate=None,
                 threshold=None,
                 calendar=None,
                 workingMinutes=None,
                 counter=None):

        #: `dict` {'count': `Number`, 'unit': :class:`.TimeUnit`},
        #: use ``set_period`` method instead setting explicitly
        self.period = period
        #: `list` of :class:`.AggregateType` objects
        self.types = types

        #: :class:`.Interpolate`
        self.interpolate = interpolate
        #: `dict` {'min': `Number`, 'max': `Number`}
        #: use ``set_threshold`` method instead setting explicitly
        self.threshold = threshold
        #: `dict` {'name': `str`}
        #: use ``set_threshold`` method instead setting explicitly
        self.calendar = calendar
        #: `dict` {'start': `int`, 'end': `int`}
        #: use ``set_workingMinutes`` method instead setting explicitly
        self.workingMinutes = workingMinutes
        #: `bool`
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

    def set_period(self, count, unit=TimeUnit.SECOND):
        """
        :param count: number
        :param unit: use :class:`.TimeUnit` enum, default TimeUnit.SECOND
        """
        if not isinstance(count, numbers.Number):
            raise ValueError('period count expected number, found: '
                             + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong period unit')
        self.period = {'count': count, 'unit': unit}

    def set_threshold(self, min, max):
        """
        :param min: `Number`
        :param max: `Number`
        """
        self.threshold = {'min': min, 'max': max}

    def set_workingMinutes(self, start, end):
        """
        :param start: `int`
        :param end: `int`
        """
        self.workingMinutes = {'start': start, 'end': end}

    def set_calendar(self, name):
        """
        :param name: `str`
        """
        self.calendar = {'name': name}


class _TimePeriodQuery(Serializable):
    def __init__(self, startTime, endTime):

        if isinstance(startTime, datetime):
            startTime = to_posix_timestamp(startTime)
        #: `long` start of the selection period.
        #: default: ``endTime - 1 hour``
        self._startTime = startTime

        if isinstance(endTime, datetime):
            endTime = to_posix_timestamp(endTime)
        #: `long` end of the selection period.
        #: default value: ``current server time``
        self._endTime = endTime

    @property
    def startTime(self):
        """`datetime` Start of the selection period
        """
        if self._startTime is None:
            return None
        return datetime.fromtimestamp(self._startTime / 1000)

    @startTime.setter
    def startTime(self, value):
        if isinstance(value, numbers.Number):
            self._startTime = value
        elif isinstance(value, datetime):
            self._startTime = to_posix_timestamp(value)
        else:
            raise ValueError('startTime should be either Number or datetime')

    @property
    def endTime(self):
        """ `datetime` End of the selection period
        """
        if self._endTime is None:
            return None
        return datetime.fromtimestamp(self._endTime / 1000)

    @endTime.setter
    def endTime(self, value):
        if isinstance(value, numbers.Number):
            self._endTime = value
        elif isinstance(value, datetime):
            self._endTime = to_posix_timestamp(value)
        else:
            raise ValueError('endTime should be either Number or datetime')


class SeriesQuery(_TimePeriodQuery):
    def rate(self):
        """add empty rate property to series query,
        use returned object methods to set parameters

        :return: :class:`.Rate` object

        Usage::

            >>> query = SeriesQuery(ENTITY, METRIC)
            >>> rate = query.rate()
            >>> rate.counter = False
            >>> series = svc.retrieve_series(query)

        """
        self._rate = Rate()
        return self._rate

    def aggregate(self, *types):
        """add aggregate property to series query, default period = 1 sec
        use returned object methods to set parameters

        :param types: :class:`.InterpolateType` objects
        :return: :class:`.Aggregator` object

        Usage::

            >>> query = SeriesQuery(ENTITY, METRIC)
            >>> aggr = query.aggregate()
            >>> aggr.set_period(10, TimeUnit.DAY)
            >>> aggr.set_types(AggregateType.MAX, AggregateType.MIN)
            >>> series = svc.retrieve_series(query)

        """

        self._aggregate = Aggregator(types,
                                     {'count': 1, 'unit': TimeUnit.SECOND})
        return self._aggregate

    def group(self, type):
        """add group property to series query
        use returned object methods to set parameters

        :param type: :class:`.AggregateType` enum
        :return: :class:`.Group` object

        Usage::

            >>> query = SeriesQuery(ENTITY, METRIC)
            >>> group = query.group(AggregateType.COUNT)
            >>> group.set_period(1, TimeUnit.SECOND)
            >>> series = svc.retrieve_series(query)

        """
        self._group = Group(type)
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
                 requestId=None,
                 versioned=None):
        #: `str` entity name
        self.entity = entity
        #: `str` metric name
        self.metric = metric

        #: `int` maximum number of data samples returned
        self.limit = limit
        #: `bool` Retrieves only 1 most recent value
        self.last = last
        #: `dict`
        self.tags = tags
        #: :class:`.SeriesType`
        self.type = type
        self._group = group
        self._rate = rate
        self._aggregate = aggregate
        #: `str`
        self.requestId = requestId
        #: `boolean`
        self.versioned = versioned

        super(SeriesQuery, self).__init__(startTime, endTime)
###################################################################################################
###################################################################################################

#===============================================================================
################# GLOBALS
#===============================================================================

class EntityFilter(Serializable):
    def __init__(self, entity="", entities=[], entity_group="", entity_expression=""):
        if (entity or entities or entity_group or entity_expression):
            self.entity = entity
            self.entities = entities
            self.entity_group=entity_group
            self.entity_expression=entity_expression
        else:
            raise ValueError("Not enough arguments")
    def get_trimmed_dict_repr(self):
        return dict((k, v) for k, v in self.__dict__.items() if v)
        
class DateFilter(Serializable):
    def __init__(self, startDate="", endDate="", interval={}):
        if interval or (startDate and endDate):
            self.startDate = startDate 
            self.endDate = endDate 
            self.interval = interval
        else:
            raise ValueError("Not enough arguments")
        
#===============================================================================
################# PROPERTIES
#===============================================================================
class PropertiesQuery(_TimePeriodQuery):
    def __init__(self, type, entity, startTime=None, endTime=None, limit=None, key=None, keyExpression=None):
        self.entity = entity
        self.type = type
        self.limit = limit
        self.key = key
        self.keyExpression = keyExpression
        super(PropertiesQuery, self).__init__(startTime, endTime)
        
class PropertiesDeleteFilter(PropertiesQuery):
    def __init__(self, type, entity, startTime=None, endTime=None, key=None, exactMatch=False):
        self.exactMatch = exactMatch
        super(PropertiesDeleteFilter, self).__init__(type, entity, startTime=startTime, endTime=endTime, limit=None, key=key, keyExpression=None)


#===============================================================================
################# ALERTS
#===============================================================================
class AlertsQuery(Serializable):
    def __init__(self, entity_filter, date_filter, alert_rules=None, alert_metrics=None, alert_severities=None, alert_minSeverity=None, alert_acknowledged=None):
        copy_not_empty_attrs(src=entity_filter, dst=self)
        copy_not_empty_attrs(src=date_filter,   dst=self)
        self.metrics = alert_metrics
        self.rules = alert_rules
        self.severities = alert_severities
        self.minSeverity = alert_minSeverity
        self.acknowledged = alert_acknowledged
        
class AlertHistoryQuery(Serializable):
    def __init__(self, entity_filter, date_filter, alert_rule, alert_metric, result_limit):
        copy_not_empty_attrs(src=entity_filter, dst=self)
        copy_not_empty_attrs(src=date_filter, dst=self)
        self.limit = result_limit
        self.rule = alert_rule
        self.metric = alert_metric
        
class AlertDeleteFilter(Serializable):
    def __init__(self, alert_id):
        self.id = alert_id

#===============================================================================
################# MESSAGES
#===============================================================================
class MessageQuery(Serializable):
    def __init__(self,entity_filter, date_filter, msg_type, msg_source, msg_tags, msg_severities, msg_minSeverity=Severity.UNDEFINED, result_limit=1000):
        """
        :param msg_type: str  Message msg_type.
        :param msg_source: str  Message msg_source.
        :param msg_tags: dict Object with name=value fields. 
        :param msg_severity: class .Severity  Severity name. 
        :param msg_severities:  An array of msg_severity codes or names. 
        :param msg_minSeverity: class .Severity  Minimum code or name msg_severity filter.
        """
        copy_not_empty_attrs(entity_filter, self)
        copy_not_empty_attrs(date_filter, self)
        self.type=msg_type
        self.source=msg_source
        self.tags=msg_tags
        self.severities=msg_severities
        self.minSeverity=msg_minSeverity

