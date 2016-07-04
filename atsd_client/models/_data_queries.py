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
        
class DateFilter(Serializable):
    def __init__(self, startDate="", endDate="", interval={}):
        if interval or (startDate and endDate):
            self.startDate = startDate 
            self.endDate = endDate 
            self.interval = interval
        else:
            raise ValueError("Not enough arguments")
#===============================================================================
################# SERIES
#===============================================================================
class SeriesQuery(Serializable):
    def __init__(self, series_filter, entity_filter, date_filter, forecast_filter=None, versioning_filter=None, control_filter=None, transformation_filter=None):
        copy_not_empty_attrs(series_filter, self)
        copy_not_empty_attrs(entity_filter, self)
        copy_not_empty_attrs(date_filter, self)
        copy_not_empty_attrs(forecast_filter, self)
        copy_not_empty_attrs(versioning_filter, self)
        copy_not_empty_attrs(transformation_filter, self)
                
class SeriesFilter(Serializable):
    def __init__(self, metric, tags={}, type="HISTORY"):
        if metric:
            self.metric = metric 
            self.tags = tags 
            self.type = type
        else:
            raise ValueError("No metric supplied!")
        
class ForecastFilter(Serializable):
    def __init__(self, forecastName=""):
        self.forecastName = forecastName
        
class VersioningFilter(Serializable):
    def __init__(self,versioned=False, versionFilter=""):
        self.versioned = versioned
        self.versionFilter = versionFilter
        
class  ControlFilter(Serializable):
    def __init__(self,limit=0, direction="DESC", last=False, cache=False, requestId="", timeFormat="iso"):
        self.limit=limit
        self.direction=direction
        self.last=last
        self.cache=cache
        self.requestId=requestId
        self.timeFormat=timeFormat

class TransformationFilter(Serializable):
    def __init__(self, aggregate, group, rate):
        self.aggregate = aggregate
        self.group = group
        self.rate = rate
        
class Transformator(Serializable):
    def __init__(self, period=None):
        self.period = period
        
    def set_period(self, count, unit=TimeUnit.SECOND):
        """
        :param count: number
        :param unit: use :class:`.TimeUnit` enum, default TimeUnit.SECOND
        """
        if not isinstance(count, numbers.Number):
            raise ValueError('period count expected number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong period unit')
        self.period = {'count': count, 'unit': unit}
        
class Rate(Transformator):
    """
    represents aggregate param rate
    """
    def __init__(self, period=None, counter=True):
        self.counter = counter
        super(Rate, self).__init__(period)

class Group(Transformator):
    """
    represents aggregate param group
    """
    def __init__(self, type, period=None, interpolate=None, truncate=None, order=0):
        self.type = type
        self.interpolate = interpolate
        self.truncate = truncate
        self.period = period
        self.order=order
        super(Group, self).__init__(period)

class Aggregator(Serializable):
    """
    represents aggregate param of :class:`.SeriesQuery`
    """
    def __init__(self, types, period, interpolate=None, threshold=None, calendar=None, workingMinutes=None, counter=None):
        self.period = period
        self.types = types
        self.interpolate = interpolate
        self.threshold = threshold
        self.calendar = calendar
        self.workingMinutes = workingMinutes
        self.counter = counter
        super(Aggregator, self).__init__(period)

    def set_types(self, *types):
        """specified aggregation types
        :param types: use :class:`.AggregateType` enum objects
        """
        self.types = []
        for typ in types:
            if not hasattr(AggregateType, typ):
                raise ValueError('wrong aggregate type')
            self.types.append(typ)

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
        
#===============================================================================
################# PROPERTIES
#===============================================================================
class PropertiesQuery(Serializable):
    #TODO
    def __init__(self, entity_filter, date_filter, type, key=None, exactMatch=False, keyTagExpression=None):
        copy_not_empty_attrs(entity_filter)
        copy_not_empty_attrs(date_filter)
        self.type = type
        self.key = key
        self.keyExpression = keyExpression
        self.limit = limit
        
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

