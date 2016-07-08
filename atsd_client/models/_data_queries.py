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
from .._utilities import copy_not_empty_attrs, to_posix_timestamp

from ._data_models import Property
from .._jsonutil import Serializable
from ._data_models import Alert

try:
    unicode = unicode
except NameError:
    unicode = str

#===============================================================================
# ###################################### Constants
#===============================================================================
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

class PeriodAlign(object):
    CALENDAR = "CALENDAR"
    START_TIME = "START_TIME"
    FIRST_VALUE_TIME = "FIRST_VALUE_TIME"
    END_TIME = "END_TIME"

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

#===============================================================================
################# General Filters
#===============================================================================
class EntityFilter(Serializable):
    def __init__(self, entity="", entities=[], entity_group="", entity_expression=""):
        if (entity or entities or entity_group or entity_expression):
            self.entity = entity
            self.entities = entities
            self.entity_group=entity_group
            self.entity_expression=entity_expression
        else:
            raise ValueError("Not enough arguments for entity filter")
        
class DateFilter(Serializable):
    def __init__(self, startDate="", endDate="", interval={}):
        if interval or (startDate and endDate):
            self.startDate = startDate 
            self.endDate = endDate 
            self.interval = interval
        else:
            raise ValueError("Not enough arguments for date filter")
#===============================================================================
################# Series Queries
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

#=======================================================================
# Transformations 
#=======================================================================
class TransformationFilter(Serializable):
    def __init__(self, aggregate, group, rate):
        self.aggregate = aggregate
        self.group = group
        self.rate = rate
        
class Rate(Serializable):
    """
    represents aggregate param rate
    """
    def __init__(self, period, counter=True):
        self.counter = counter
        self.period = period
        
    def set_period(self, count, unit=TimeUnit.SECOND):
        if not isinstance(count, numbers.Number):
            raise ValueError('period count expected number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong period unit')
        self.period = {'count' : count, 'unit' : unit}
    
    def set_counter(self, counter):
        if isinstance(counter, bool):
            self.counter = counter
        else:
            raise ValueError('wrong counter')

class Group(Serializable):
    def __init__(self, type, period=None, interpolate=None, truncate=False, order=0):
        self.type = type
        if period is not None:
            self.set_period(**period)
        if interpolate is not None:
            self.set_interpolate(**interpolate)
        self.truncate = truncate
        self.set_truncate(truncate)
        self.set_order(order)

    def set_type(self, value):
        if not hasattr(AggregateType, value):
            raise ValueError('wrong type parameter, expected Interpolate, found: ' + unicode(type(value)))
        self.type = value

    def set_period(self, count, unit=TimeUnit.SECOND, align=PeriodAlign.CALENDAR):
        if not isinstance(count, numbers.Number):
            raise ValueError('period count expected number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong period unit parameter; should be TimeUnit, found: ' + unicode(type(value)))
        if not hasattr(PeriodAlign, align):
            raise ValueError('wrong align parameter; should be PeriodAlign, found: ' + unicode(type(value)))
        self.period = {'count' : count, 'unit' : unit, 'align' : align}

    def set_interpolate(self, type, value=None, extend=False):
        if not isinstance(type, numbers.Number):
            raise ValueError('wrong interpolate parameter, expected number, found: ' + unicode(type(type)))
        self.interpolate = {'type' : type}
        if value is not None:
            if not isinstance(value, numbers.Number):
                raise ValueError('wrong value parameter, expected number, found: ' + unicode(type(value)))
            self.interpolate['value'] = value
        if not isinstance(extend, bool):
            raise ValueError('wrong extend parameter, expected boolean, found: ' + unicode(type(extend)))
        self.interpolate['extend'] = extend

    def set_truncate(self, value):
        if not isinstance(value, bool):
            raise ValueError("wrong truncate parameter; should be boolean, found: " + unicode(type(value))) 
        self.truncate = value

    def set_order(self, value):
        if not isinstance(value, numbers.Number):
            raise ValueError("wrong order parameter; should be number, found: " + unicode(type(value))) 
        self.order = value


class Aggregate(Serializable):
    def __init__(self, period, types=[AggregateType.DETAIL], interpolate=None, threshold=None, calendar=None, workingMinutes=None, order=1):
        self.set_types(*types)
        if interpolate is not None:
            self.set_interpolate(**interpolate)
        if calendar is not None:
            self.set_calendar(**calendar)
        if workingMinutes is not None:
            self.set_workingMinutes(**workingMinutes)
        if threshold is not None:
            self.set_threshold(**threshold)
        if period is not None:
            self.set_period(**period)
        if order is not None:
            self.set_order(order)

    def set_types(self, *types):
        self.types = []
        for typ in types:
            if not hasattr(AggregateType, typ):
                raise ValueError('wrong aggregate type; should be AggregateType, found: ' + unicode(type(value)))
            self.types.append(typ)

    def set_threshold(self, min, max):
        if not isinstance(min, numbers.Number) or not isinstance(max, numbers.Number):
            raise ValueError('wrong threshold parameters; should be numbers, found: min(' + unicode(type(min)) + ') end(' + unicode(type(max)))
        self.threshold = {'min': min, 'max': max}

    def set_workingMinutes(self, start, end):
        if not isinstance(start, numbers.Number) or not isinstance(end, numbers.Number):
            raise ValueError('wrong workinMinutes parameters; should be numbers, found: start(' + unicode(type(start)) + ') end(' + unicode(type(end)))
        self.workingMinutes = {'start': start, 'end': end}

    def set_calendar(self, name):
        if not isinstance(name, str):
            raise ValueError("wrong name parameter; should be string, found: " + unicode(type(name)))
        self.calendar = {'name': name}
    
    def set_period(self, count, unit=TimeUnit.SECOND, align=PeriodAlign.CALENDAR):
        if not isinstance(count, numbers.Number):
            raise ValueError('period count expected number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('wrong period unit')
        self.period = {'count' : count, 'unit' : unit}
        if align is not None:
            self.period['align'] = align
            
    def set_interpolate(self, type, value=None, extend=False):
        if not hasattr(Interpolate, type) and not isinstance(value, numbers.Number):
            raise ValueError('wrong type parameter, expected Interpolate, found: ' + unicode(type(type)))
        self.interpolate = {'type' : type}
        if value is not None:
            if not isinstance(value, numbers.Number):
                raise ValueError('wrong value parameter, expected number, found: ' + unicode(type(value)))
            self.interpolate['value'] = value
        if not isinstance(extend, bool):
            raise ValueError('wrong extend parameter, expected boolean, found: ' + unicode(type(extend)))
        self.interpolate['extend'] = extend
                
    def set_order(self, order):
        if not isinstance(order, numbers.Number):
            raise ValueError('wrong order, expected number, found: ' + unicode(type(order)))
#===============================================================================
################# Properties
#===============================================================================
class PropertiesQuery(Serializable):
    def __init__(self, entity_filter, date_filter, type, key=None, exactMatch=False, keyTagExpression=None, limit=0, last=False, offset=-1):
        copy_not_empty_attrs(entity_filter, self)
        copy_not_empty_attrs(date_filter, self)
        self.type=type
        self.key=key
        self.exactMatch=exactMatch
        self.keyTagExpression=keyTagExpression
        self.limit=limit
        self.last=last
        self.offset=offset
        
class PropertiesDeleteFilter(Serializable):
    def __init__(self, type, entity, startTime=None, endTime=None, key=None, exactMatch=False):
        self.type=type
        self.entity=entity
        self.startTime=startTime
        self.endTime=endTime
        self.key=key
        self.exactMatch=exactMatch

#===============================================================================
################# Alerts
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
################# Messages
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
