# -*- coding: utf-8 -*-

"""
Copyright 2018 Axibase Corporation or its affiliates. All Rights Reserved.

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
from .._utilities import copy_not_empty_attrs
from .._time_utilities import to_iso

unicode = str


# ===============================================================================
# ###################################### Constants
# ===============================================================================
class SeriesType(object):
    HISTORY = 'HISTORY'
    FORECAST = 'FORECAST'
    FORECAST_DEVIATION = 'FORECAST_DEVIATION'


# ------------------------------------------------------------------------------
class InterpolateType(object):
    NONE = 'NONE'
    PREVIOUS = 'PREVIOUS'
    NEXT = 'NEXT'
    LINEAR = 'LINEAR'
    VALUE = 'VALUE'


# ------------------------------------------------------------------------------
class InterpolateFunction(object):
    AUTO = 'AUTO'
    LINEAR = 'LINEAR'
    PREVIOUS = 'PREVIOUS'


# ------------------------------------------------------------------------------
class InterpolateBoundary(object):
    INNER = 'INNER'
    OUTER = 'OUTER'


# ------------------------------------------------------------------------------
class TimeUnit(object):
    NANOSECOND = 'NANOSECOND'
    MILLISECOND = 'MILLISECOND'
    SECOND = 'SECOND'
    MINUTE = 'MINUTE'
    HOUR = 'HOUR'
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    QUARTER = 'QUARTER'
    YEAR = 'YEAR'


# ------------------------------------------------------------------------------
class PeriodAlign(object):
    CALENDAR = "CALENDAR"
    START_TIME = "START_TIME"
    FIRST_VALUE_TIME = "FIRST_VALUE_TIME"
    END_TIME = "END_TIME"


# ------------------------------------------------------------------------------
class AggregateType(object):
    DETAIL = 'DETAIL'
    COUNT = 'COUNT'
    COUNTER = 'COUNTER'
    MIN = 'MIN'
    MAX = 'MAX'
    MIN_VALUE_TIME = 'MIN_VALUE_TIME'
    MAX_VALUE_TIME = 'MAX_VALUE_TIME'
    AVG = 'AVG'
    SUM = 'SUM'
    PERCENTILE_999 = 'PERCENTILE_999'
    PERCENTILE_995 = 'PERCENTILE_995'
    PERCENTILE_99 = 'PERCENTILE_99'
    PERCENTILE_95 = 'PERCENTILE_95'
    PERCENTILE_90 = 'PERCENTILE_90'
    PERCENTILE_75 = 'PERCENTILE_75'
    PERCENTILE_50 = 'PERCENTILE_50'
    MEDIAN = 'MEDIAN'
    STANDARD_DEVIATION = 'STANDARD_DEVIATION'
    FIRST = 'FIRST'
    LAST = 'LAST'
    DELTA = 'DELTA'
    WAVG = 'WAVG'
    WTAVG = 'WTAVG'
    THRESHOLD_COUNT = 'THRESHOLD_COUNT'
    THRESHOLD_DURATION = 'THRESHOLD_DURATION'
    THRESHOLD_PERCENT = 'THRESHOLD_PERCENT'


# ------------------------------------------------------------------------------
class Severity(object):
    UNDEFINED = 0
    UNKNOWN = 1
    NORMAL = 2  # INFO
    WARNING = 3  # WARN
    MINOR = 4
    MAJOR = 5
    CRITICAL = 6  # ERROR
    FATAL = 7

# ------------------------------------------------------------------------------
class SmoothType(object):
    AVG = "AVG"
    COUNT = "COUNT"
    SUM = "SUM"
    WAVG = "WAVG"
    WTAVG = "WTAVG"
    EMA = "EMA"

# ------------------------------------------------------------------------------
class DownsampleAlgorithm(object):
    DETAIL = "DETAIL"
    INTERPOLATE = "INTERPOLATE"

# ------------------------------------------------------------------------------
class EvaluateMode(object):
    STRICT = "STRICT"
    NOT_STRICT = "NOT_STRICT"

# ------------------------------------------------------------------------------
class DecomposeMethod(object):
    FULL = "FULL"
    TRUNCATED = "TRUNCATED"
    AUTO = "AUTO"

# ------------------------------------------------------------------------------
class ReconstructAveragingFunction(object):
    AVG = "AVG"
    MEDIAN = "MEDIAN"

# ------------------------------------------------------------------------------
class SsaForecastMethod(object):
    RECURRENT = "RECURRENT"
    VECTOR = "VECTOR"

# ------------------------------------------------------------------------------
class SsaForecastBase(object):
    RECONSTRUCTED = "RECONSTRUCTED"
    ORIGINAL = "ORIGINAL"

# ------------------------------------------------------------------------------
class SsaGroupAutoClusteringMethod(object):
    HIERARCHICAL = "HIERARCHICAL"
    XMEANS = "XMEANS"
    NOVOSIBIRSK = "NOVOSIBIRSK"

# ===============================================================================
# General Filters
# ===============================================================================
class EntityFilter():
    """
    Helper class to retrieve a list of entities for the specified filters.
    One of the entity arguments is required.
    Entity name pattern supports ? and * wildcards.
    Filter precedence, from high to low: entity, entities, entityGroup. Although multiple filters can be specified in the same query object only the filter with the highest precedence is applied.
    Entity expression is applied as an additional filter to the list of entities retrieved by the above filters.
    """

    def __init__(self, entity, entities=None, entity_group=None, entity_expression=None):
        if not entity:
            raise ValueError("Entity is required.")
        #: `str` entity name or entity name pattern.
        self.entity = entity
        #: `list` of entity names or entity name patterns
        self.entities = [] if entities is None else entities
        #: `str` entity group name. Returns records for member entities of the specified group.
        # The result is empty if the group doesn't exist or contains no entities.
        self.entity_group = None if entity_group is None else entity_group
        #: `str` filter entities by name, field, entity tag, and properties
        self.entity_expression = None if entity_expression is None else entity_expression

    def set_entity(self, value):
        self.entity = value

    def set_entities(self, value):
        self.entities = value

    def set_entity_group(self, value):
        self.entity_group = value

    def set_entity_expression(self, value):
        self.entity_expression = value


# ------------------------------------------------------------------------------
class DateFilter:
    def _validate(self):
        return (self.startDate is not None and self.endDate is not None) or \
               (self.interval is not None) and all(key in self.interval for key in ("count", "unit"))

    def __init__(self, start_date=None, end_date=None, interval=None):
        #: :class:`datetime` object | `long` milliseconds | `str` ISO 8601 date. Start of the selection interval.
        # Matches samples timestamped at or after the startDate. Examples: 2018-07-18T11:11:02Z, current_hour
        self.startDate = to_iso(start_date)
        #: :class:`datetime` object | `long` milliseconds | `str` ISO 8601 date. End of the selection interval.
        # Matches records timestamped before the endDate. Examples: 2018-07-18T11:11:02+02:00, previous_day - 1 * HOUR
        self.endDate = to_iso(end_date)
        #: `dict`. Duration of the selection interval, specified as count and unit.
        # Example: {"count": 5, "unit": "MINUTE"}
        self.interval = interval
        if not self._validate():
            raise ValueError(
                "Invalid arguments for the date filter: startDate={}, endDate={}, interval={}".format(start_date,
                                                                                                      end_date,
                                                                                                      interval))

    def set_start_date(self, value):
        self.startDate = to_iso(value)

    def set_end_date(self, value):
        self.endDate = to_iso(value)

    def set_interval(self, value):
        self.interval = value


# ===============================================================================
# Series Queries
# ===============================================================================
class SeriesQuery:
    """
    Class representing a series query to get sample for the specified filters and parameters.
    """

    def __init__(self, series_filter, entity_filter, date_filter, forecast_filter=None, versioning_filter=None,
                 control_filter=None, transformation_filter=None, sample_filter=None, subseries_filter=None):
        copy_not_empty_attrs(series_filter, self)
        copy_not_empty_attrs(entity_filter, self)
        copy_not_empty_attrs(date_filter, self)
        copy_not_empty_attrs(forecast_filter, self)
        copy_not_empty_attrs(versioning_filter, self)
        copy_not_empty_attrs(transformation_filter, self)
        copy_not_empty_attrs(control_filter, self)
        copy_not_empty_attrs(sample_filter, self)
        if subseries_filter is not None:
            self.series = [subseries_filter] if not isinstance(subseries_filter, list) else subseries_filter
        if (not hasattr(self, "metric")) and (not hasattr(self, "metrics")) and (not hasattr(self, "series")):
            raise ValueError('One of the followind params required: metric, metrics or series')

    def set_series_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_entity_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_date_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_forecast_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_versioning_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_control_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_transformation_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_sample_filter(self, value):
        copy_not_empty_attrs(value, self)


# ------------------------------------------------------------------------------
class SeriesDeleteQuery:
    """
    Class representing a series delete query for the specified entity, metric and series tags.
    """

    def __init__(self, entity, metric, tags=None, exact_match=None):
        if not metric:
            raise ValueError("Metric is required.")
        if not entity:
            raise ValueError("Entity is required.")
        #: `str` metric name
        self.metric = metric
        #: `str` entity name
        self.entity = entity
        #: `dict` series tags
        self.tags = tags
        # : `bool` tags match operator: exact match if true, partial match if false
        self.exactMatch = True if exact_match is None else exact_match

    def set_metric(self, value):
        self.metric = value

    def set_entity(self, value):
        self.entity = value

    def set_tags(self, value):
        self.tags = value

    def set_exact_match(self, value):
        self.exactMatch = value


# ------------------------------------------------------------------------------
class SeriesFilter:
    def __init__(self, metric=None, tags=None, type="HISTORY", tag_expression=None, exact_match=None, metrics=None):
        #if ( not metric ) and ( not metrics ):
        #   raise ValueError("Metric is required.")
        #: `str` metric name
        self.metric = metric
        #: `dict`
        self.tags = {} if tags is None else tags
        #: :class:`.SeriesType` type of underlying data: HISTORY, FORECAST, FORECAST_DEVIATION. Default: HISTORY
        self.type = type
        #: `str` tag expression to include series that match the specified tag condition
        self.tagExpression = tag_expression
        # : `bool` tags match operator: exact match if true, partial match if false
        self.exactMatch = False if exact_match is None else exact_match
        if metrics is not None:
            self.metrics = metrics

    def set_metric(self, value):
        self.metric = value

    def set_tags(self, value):
        self.tags = value

    def set_type(self, value):
        self.type = value

    def set_tag_expression(self, value):
        self.tagExpression = value

    def set_exact_match(self, value):
        self.exactMatch = value

    def set_metrics(self, value):
        self.metrics = value


# ------------------------------------------------------------------------------
class ForecastFilter:
    def __init__(self, forecast_name=""):
        # : `str` unique forecast name. Identifies a custom forecast by name. If forecastName is not set,
        # then the default forecast computed by the database is returned. forecastName is applicable only when
        # type is set to FORECAST or FORECAST_DEVIATION
        self.forecastName = forecast_name

    def set_forecast_name(self, value):
        self.forecastName = value


# ------------------------------------------------------------------------------
class VersioningFilter:
    def __init__(self, versioned=None, version_filter=None):
        # : `bool` option indicating if version status, source, and change date is returned if metric is
        # versioned. Default: false.
        self.versioned = False if versioned is None else versioned
        # : `str` expression to filter value history (versions) by version status, source or time, for example:
        # version_status = 'Deleted' or version_source LIKE '*user*'
        self.versionFilter = "" if version_filter is None else version_filter


# ------------------------------------------------------------------------------
class ControlFilter:
    def __init__(self, limit=None, direction=None, series_limit=None, cache=None, request_id=None, time_format=None,
                 add_meta=None):
        #: `int` maximum number of time:value samples returned for each series. Default: 0.
        self.limit = 0 if limit is None else limit
        #: `str` scan order for applying the limit: DESC - descending, ASC - ascending. Default: DESC
        self.direction = "DESC" if direction is None else direction
        #: `int` maximum number of series returned. Default: 0.
        self.seriesLimit = 0 if series_limit is None else series_limit
        # : `bool` option. If true, execute the query against Last Insert table which results in faster response time
        # for last value queries. Default: false
        self.cache = False if cache is None else cache
        #: `str` optional identifier used to associate query object in request with series objects in response.
        self.requestId = "" if request_id is None else request_id
        #: `str` time format for data array. iso or milliseconds. Default: iso
        self.timeFormat = "iso" if time_format is None else time_format
        # : `bool` option. If true, include metric and entity metadata (field, tags) under the meta object in response.
        # Default: false
        self.addMeta = False if add_meta is None else add_meta

    def set_limit(self, value):
        self.limit = value

    def set_direction(self, value):
        self.direction = value

    def set_cache(self, value):
        self.cache = value

    def set_request_id(self, value):
        self.requestId = value

    def set_time_format(self, value):
        self.timeFormat = value

    def set_series_limit(self, value):
        self.seriesLimit = value

    def set_add_meta(self, value):
        self.addMeta = value


# ------------------------------------------------------------------------------
class SampleFilter:
    def __init__(self, sampleFilter=""):
        # Boolean expression applied to each time:value sample.
        # Samples that satisfy the condition are included in the result.
        # Docs: https://axibase.com/docs/atsd/api/data/series/query.html#sample-filter
        self.sampleFilter = "" if sampleFilter is None else sampleFilter


# ------------------------------------------------------------------------------
class SubseriesFilter:
    def __init__(self, name, seriesFilter=None, entityFilter=None):
        self.name = name
        if seriesFilter is not None:
            copy_not_empty_attrs(seriesFilter, self)
            self.type = None
        if entityFilter is not None:
            copy_not_empty_attrs(entityFilter, self)

    def set_series_filter(self, seriesFilter):
        if not isinstance(seriesFilter, SeriesFilter):
            raise ValueError('Incorrect series filter, expected instance of SeriesFilter class, found: ' + unicode(type(seriesFilter)))
        copy_not_empty_attrs(seriesFilter, self)
        self.type = None

    def set_entity_filter(self, entityFilter):
        if not isinstance(entityFilter, EntityFilter):
            raise ValueError('Incorrect series filter, expected instance of EntityFilter class, found: ' + unicode(type(entityFilter)))
        copy_not_empty_attrs(entityFilter, self)

# =======================================================================
# Transformations 
# =======================================================================
class TransformationFilter:
    def __init__(self, aggregate=None, group=None, rate=None, interpolate=None, smooth=None, downsample=None, evaluate=None, forecast=None):

        # : :class:`.Aggregate` object responsible for grouping detailed values into periods and calculating
        # statistics for each period. Default: DETAIL
        self.aggregate = aggregate
        #: :class:`.Group` object responsible for merging multiple series into one series
        self.group = group
        # : :class:`.Rate` object responsible for computing difference between consecutive samples per unit of time (
        # rate period)
        self.rate = rate
        self.interpolate = interpolate
        self.smooth = smooth
        self.downsample = downsample
        self.evaluate = evaluate
        self.forecast = forecast

    def set_aggregate(self, value):
        self.aggregate = value

    def set_group(self, value):
        self.group = value

    def set_rate(self, value):
        self.rate = value

    def set_interpolate(self, value):
        self.interpolate = value

    def set_smooth(self, value):
        self.smooth = value

    def set_downsample(self, value):
        self.downsample = value

    def set_evaluate(self, value):
        self.evaluate = value

    def set_forecast(self, value):
        self.forecast = value


# ------------------------------------------------------------------------------
class Rate:
    """
    Class representing aggregate param 'rate'
    """

    def __init__(self, period=None, counter=True):
        self.counter = counter
        self.period = period

    def set_period(self, count, unit=TimeUnit.SECOND):
        if not isinstance(count, numbers.Number):
            raise ValueError('Period count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid period unit')
        self.period = {'count': count, 'unit': unit}

    def set_counter(self, counter):
        if isinstance(counter, bool):
            self.counter = counter
        else:
            raise ValueError('Invalid counter')


# ------------------------------------------------------------------------------
class Group:
    """
    Class representing aggregate param 'group'
    """

    def __init__(self, type, period=None, interpolate=None, truncate=None, order=None):
        self.set_type(type)
        self.set_truncate(truncate)
        self.set_order(order)
        if period is not None:
            self.set_period(**period)
        if interpolate is not None:
            self.set_interpolate(**interpolate)

    def set_type(self, value):
        if not hasattr(AggregateType, value):
            raise ValueError('Invalid type parameter, expected AggregateType, found: ' + unicode(type(value)))
        self.type = value

    def set_period(self, count, unit=TimeUnit.SECOND):
        if not isinstance(count, numbers.Number):
            raise ValueError('Period count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid period unit parameter; must be TimeUnit, found: ' + unicode(type(unit)))
        self.period = {'count': count, 'unit': unit}

    def set_interpolate(self, type, value=None, extend=False):
        if not hasattr(InterpolateType, type):
            raise ValueError('Invalid interpolate parameter, must be an InterpolateType, found: ' + unicode(type(type)))
        self.interpolate = {'type': type}
        if value is not None:
            if not isinstance(value, numbers.Number):
                raise ValueError('Invalid value parameter, must be a number, found: ' + unicode(type(value)))
            self.interpolate['value'] = value
        if not isinstance(extend, bool):
            raise ValueError('Invalid extend parameter, must be a number, found: ' + unicode(type(extend)))
        self.interpolate['extend'] = extend

    def set_truncate(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("Invalid truncate parameter, must be a boolean, found: " + unicode(type(value)))
        self.truncate = value if value is not None else False

    def set_order(self, value):
        if value is not None and not isinstance(value, numbers.Number):
            raise ValueError("Invalid order parameter, must be a number, found: " + unicode(type(value)))
        self.order = value if value is not None else 0


class Aggregate:
    """
    Class representing aggregate param 'aggregate'
    """

    def __init__(self, period, types=None, interpolate=None, threshold=None, calendar=None, working_minutes=None,
                 order=None):
        if types is not None:
            self.set_types(*types)
        else:
            self.types = [AggregateType.DETAIL]
        if interpolate is not None:
            self.set_interpolate(**interpolate)
        if calendar is not None:
            self.set_calendar(**calendar)
        if working_minutes is not None:
            self.set_working_minutes(**working_minutes)
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
                raise ValueError('Invalid aggregate type; must be AggregateType, found: ' + unicode(type(typ)))
            self.types.append(typ)

    def set_threshold(self, min, max):
        if not isinstance(min, numbers.Number) or not isinstance(max, numbers.Number):
            raise ValueError(
                'Invalid threshold parameters, must be a number, found: min(' + unicode(type(min)) + ') end(' + unicode(
                    type(max)))
        self.threshold = {'min': min, 'max': max}

    def set_working_minutes(self, start, end):
        if not isinstance(start, numbers.Number) or not isinstance(end, numbers.Number):
            raise ValueError('Invalid workingMinutes parameters, must be a number, found: start(' + unicode(
                type(start)) + ') end(' + unicode(type(end)))
        self.workingMinutes = {'start': start, 'end': end}

    def set_calendar(self, name):
        if not isinstance(name, str):
            raise ValueError("Invalid name parameter, must be a string, found: " + unicode(type(name)))
        self.calendar = {'name': name}

    def set_period(self, count, unit=TimeUnit.SECOND, align=PeriodAlign.CALENDAR, timezone=None):
        if not isinstance(count, numbers.Number):
            raise ValueError('Period count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid period unit')
        self.period = {'count': count, 'unit': unit}
        if align is not None:
            self.period['align'] = align
        if timezone is not None:
            self.period['timezone'] = timezone

    def set_interpolate(self, type, value=None, extend=False):
        if not hasattr(InterpolateType, type) and not isinstance(value, numbers.Number):
            raise ValueError('Invalid type parameter, expected InterpolateType, found: ' + unicode(type(type)))
        self.interpolate = {'type': type}
        if value is not None:
            if not isinstance(value, numbers.Number):
                raise ValueError('Invalid value parameter, must be a number, found: ' + unicode(type(value)))
            self.interpolate['value'] = value
        if not isinstance(extend, bool):
            raise ValueError('Invalid extend parameter, must be a boolean, found: ' + unicode(type(extend)))
        self.interpolate['extend'] = extend

    def set_order(self, order):
        if not isinstance(order, numbers.Number):
            raise ValueError('Invalid order, must be a number, found: ' + unicode(type(order)))
        self.order = order if order is not None else 0


class Interpolate:
    """
    Class representing aggregate param 'interpolate'
    """

    def __init__(self, period, function, boundary=None, fill=None):
        if period is not None:
            self.set_period(**period)
        if function is not None:
            self.set_function(function)
        if boundary is not None:
            self.set_boundary(boundary)
        if fill is not None:
            self.set_fill(fill)

    def set_period(self, count, unit=TimeUnit.SECOND, align=None, timezone=None):
        if not isinstance(count, numbers.Number):
            raise ValueError('Period count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid period unit')
        self.period = {'count': count, 'unit': unit}
        if align is not None:
            self.period['align'] = align
        if timezone is not None:
            self.period['timezone'] = timezone

    def set_function(self, function):
        if not hasattr(InterpolateFunction, function):
            raise ValueError(
                'Invalid function parameter, expected InterpolateFunction, found: ' + unicode(type(function)))
        self.function = function

    def set_boundary(self, boundary):
        if not hasattr(InterpolateBoundary, boundary):
            raise ValueError(
                'Invalid boundary parameter, expected InterpolateBoundary, found: ' + unicode(type(boundary)))
        self.boundary = boundary

    def set_fill(self, fill):
        if not isinstance(fill, (bool, numbers.Number)):
            raise ValueError('Invalid fill parameter, expected bool or number, found: ' + unicode(type(fill)))
        self.fill = fill


class Smooth:
    """
    Class representing transformation param 'smooth'
    """

    def __init__(self, smoothType, count=None, interval=None, minimumCount=None, incompleteValue=None):
        if not hasattr(SmoothType, smoothType):
            raise ValueError('Invalid type parameter, expected SmoothType, found: ' + unicode(type(smoothType)))
        self.type = smoothType
        if count is not None:
            self.count = count
        if interval is not None:
            self.interval = interval
        if minimumCount is not None:
            self.minimumCount = minimumCount
        if incompleteValue is not None:
            self.incompleteValue = incompleteValue

    def set_type(self, smoothType):
        if not hasattr(SmoothType, smoothType):
            raise ValueError('Invalid type parameter, expected SmoothType, found: ' + unicode(type(smoothType)))
        self.type = smoothType

    def set_count(self, count):
        if not isinstance(count, numbers.Number):
            raise ValueError('Count must be a number, found: ' + unicode(type(count)))
        self.count = count

    def set_interval(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Interval count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid interval unit')
        self.interval = {'count': count, 'unit': unit}

    def set_minimumCount(self, minimumCount):
        if not isinstance(minimumCount, numbers.Number):
            raise ValueError('Minimum count must be a value, found: ' + unicode(type(minimumCount)))
        self.minimumCount = minimumCount

    def set_incompleteValue(self, incompleteValue):
        if not isinstance(incompleteValue, str):
            raise ValueError('Incomplete value must be string, found: ' + unicode(type(incompleteValue)))
        self.incompleteValue = incompleteValue


class Downsample:
    """
    Class representing aggregate param 'downsample'
    """

    def __init__(self, algorithm=None, difference=None, ratio=None, gap=None):
        if algorithm is not None:
            self.algorithm = algorithm
        if difference is not None:
            self.difference = difference
        if ratio is not None:
            self.ratio = ratio
        if gap is not None:
            self.gap = gap

    def set_algorithm(self, algorithm):
        if not hasattr(DownsampleAlgorithm, algorithm):
            raise ValueError('Invalid algorithm parameter, expected DownsampleAlgorithm, found: ' + str(algorithm))
        self.algorithm = algorithm

    def set_difference(self, difference):
        if not isinstance(difference, numbers.Number):
            raise ValueError('Invalid difference parameter, expected number, found: ' + unicode(type(difference)))
        self.difference = difference

    def set_ratio(self, ratio):
        if not isinstance(ratio, numbers.Number):
            raise ValueError('Invalid ratio parameter, expected number, found: ' + unicode(type(ratio)))
        self.ratio = ratio

    def set_gap(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Gap count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid gap unit ' + str(unit))
        self.gap = {'count': count, 'unit': unit}


class Evaluate:
    """
    Class representing aggregate param 'evaluate'
    """

    def __init__(self, mode=None, libs=None, expression=None, script=None, order=None, timezone=None):
        if mode is not None:
            self.mode = mode
        if libs is not None:
            self.libs = [libs] if not isinstance(libs, list) else libs
        if expression is not None:
            self.expression = expression
        if script is not None:
            self.script = script
        if order is not None:
            self.order = order
        if timezone is not None:
            self.timezone = timezone

    def set_mode(self, mode):
        if not hasattr(EvaluateMode, mode):
            raise ValueError('Mode must be one of EvaluateMode attributes, found: ' + str(mode))
        self.mode = mode

    def set_libs(self, libs):
        self.libs = [libs] if not isinstance(libs, list) else libs

    def set_expression(self, expression):
        self.expression = expression

    def set_script(self, script):
        self.script = script

    def set_order(self, order):
        if not isinstance(order, numbers.Number):
            raise ValueError('Order must be a number, found: ' + unicode(type(order)))
        self.order = order

    def set_timezone(self, timezone):
        self.timezone = timezone


# =======================================================================
# Forecast Transformation
# =======================================================================
class ForecastTransformation:

    def __init__(self, autoAggregate=None, aggregationFunction=None, include=None, scoreInterval=None, forecastRange=None,
                    holtwinters=None, arima=None, ssa=None):
        if autoAggregate is not None:
            self.autoAggregate = autoAggregate
        if aggregationFunction is not None:
            self.aggregationFunction = aggregationFunction
        if include is not None:
            self.include =[include] if not isinstance(include, list) else include
        if scoreInterval is not None:
            self.scoreInterval = scoreInterval
        if forecastRange is not None:
            self.range = forecastRange
        if holtwinters is not None:
            self.hw = holtwinters
        if arima is not None:
            self.arima = arima
        if ssa is not None:
            self.ssa = ssa

    def set_auto_aggregate(self, autoAggregate):
        if not isinstance(autoAggregate, bool):
            raise ValueError('AutoAggregate expected to be bool, found: ' + unicode(type(autoAggregate)))
        self.autoAggregate = autoAggregate

    def set_aggregation_function(self, aggregationFunction):
        if not hasattr(AggregateType, aggregationFunction):
            raise ValueError('Expected one of AggregateType attributes, found: ' + str(aggregationFunction))
        self.aggregationFunction= aggregationFunction

    def set_include(self, include):
        self.include =[include] if not isinstance(include, list) else include

    def set_score_interval(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Score Interval count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid score interval unit, found: ' + str(unit))
        self.scoreInterval = {'count': count, 'unit': unit}

    def set_range(self, minRange, maxRange):
        if not isinstance(minRange, numbers.Number):
            raise ValueError('Expected min to be a number, found: ' + unicode(type(minRange)))
        if not isinstance(minRange, numbers.Number):
            raise ValueError('Expected max to be a number, found: ' + unicode(type(maxRange)))
        self.range = {'min': minRange, 'max': maxRange}

    def set_holtwinters(self, holtwinters):
        if not isinstance(holtwinters, HoltWinters):
            raise ValueError('Expected HolwWinters class instance, found: ' + unicode(type(holtwinters)))
        self.hw = holtwinters

    def set_arima(self, arima):
        if not isinstance(arima, Arima):
            raise ValueError('Expected Arima class instance, found: ' + unicode(type(arima)))
        self.arima = arima

    def set_ssa(self, ssa):
        if not isinstance(ssa, Ssa):
            raise ValueError('Expected SSA class instance, found: ' + unicode(type(ssa)))
        self.ssa = ssa


class HoltWinters:

    def __init__(self, interval=None, length=None, endDate=None, startDate=None):
        if interval is not None:
            self.interval = None
        if length is not None:
            self.length = length
        if endDate is not None:
            self.endDate = endDate
        if startDate is not None:
            self.startDate = startDate

    def set_interval(self, count, unit):
        if not isinstance(count, numbers.Number):
            raise ValueError('Interval count must be a number, found: ' + unicode(type(count)))
        if not hasattr(TimeUnit, unit):
            raise ValueError('Invalid interval unit, found: ' + str(unit))
        self.scoreInterval = {'count': count, 'unit': unit}

    def set_length(self, length):
        if not isinstance(length, numbers.Number):
            raise ValueError('Length expected to be a number, found: ' + unicode(type(length)))
        self.length = length

    def set_end_date(self, endDate):
        self.endDate = endDate

    def set_start_date(self, startDate):
        self.startDate = startDate


class Arima:

    def __init__(self, auto=None, p=None, d=None):
        if auto is not None:
            self.auto = auto
        if p is not None:
            self.p = p
        if d is not None:
            self.d = d

    def set_auto(self, auto):
        if not isinstance(auto, bool):
            raise ValueError('Auto parameter must be bool, but found: ' + unicode(type(auto)))
        self.auto = auto

    def set_p(self, p):
        if not isinstance(p, numbers.Number):
            raise ValueError('P must be a number, but found: ' + unicode(type(p)))
        self.p = p

    def set_d(self, d):
        if not isinstance(d, numbers.Number):
            raise ValueError('D must be a number, but found: ' + unicode(type(d)))
        self.d = d


class Ssa:

    def __init__(self, decompose=None, group=None, reconstruct=None, ssaForecast=None):
        if decompose is not None:
            self.decompose = decompose
        if group is not None:
            self.group = group
        if reconstruct is not None:
            self.reconstruct = reconstruct
        if ssaForecast is not None:
            self.forecast = ssaForecast

    def set_decompose(self, decompose):
        if not isinstance(decompose, Decompose):
            raise ValueError('Expected Decompose class instance, found: ' + unicode(type(decompose)))
        self.decompose = decompose

    def set_reconstruct(self, reconstruct):
        if not isinstance(reconstruct, Reconstruct):
            raise ValueError('Expected Reconstruct class instance, found: ' + unicode(type(reconstruct)))
        self.reconstruct = reconstruct

    def set_forecast(self, ssaForecast):
        if not isinstance(ssaForecast, SsaForecast):
            raise ValueError('Expected SsaForecast class instance, found: ' + unicode(type(ssaForecast)))
        self.forecast = ssaForecast

    def set_group(self, group):
        if not isinstance(group, SsaGroup):
            raise ValueError('Expected SsaGroup class instance, found: ' + unicode(type(group)))
        self.group = group


class Decompose:

    def __init__(self, eigentripleLimit=None, method=None, windowLength=None, singularValueThreshold=None):
        if eigentripleLimit is not None:
            self.eigentripleLimit = eigentripleLimit
        if method is not None:
            self.method = method
        if windowLength is not None:
            self.windowLength = windowLength
        if singularValueThreshold is not None:
            self.singularValueThreshold = singularValueThreshold

    def set_eigentriple_limit(self, eigentripleLimit):
        if not isinstance(eigentripleLimit, numbers.Number):
            raise ValueError('Expected a number on eigentripleLimit, but found: ' + unicode(type(eigentripleLimit)))
        self.eigentripleLimit = eigentripleLimit

    def set_method(self, method):
        if not hasattr(DecomposeMethod, method):
            raise ValueError('Expected attribute from DecomposeMethod, but found' + str(method))
        self.method = method

    def set_window_length(self, windowLength):
        if not isinstance(windowLength, numbers.Number):
            raise ValueError('Expected a number on windowLength, but found: ' + unicode(type(windowLength)))
        self.windowLength = windowLength

    def set_singular_value_threshold(self, singularValueThreshold):
        if not isinstance(singularValueThreshold, numbers.Number):
            raise ValueError('Expected a number on singularValueThreshold, but found: ' + unicode(type(singularValueThreshold)))
        self.singularValueThreshold = singularValueThreshold


class Reconstruct:

    def __init__(self, averagingFunction=None, fourier=None):
        if averagingFunction is not None:
            self.averagingFunction = averagingFunction
        if fourier is not None:
            self.fourier = fourier

    def set_averaging_function(self, averagingFunction):
        if not hasattr(ReconstructAveragingFunction, averagingFunction):
            raise ValueError('Expected attribute of ReconstructAveragingFunction, found: ' + str(averagingFunction))
        self.averagingFunction = averagingFunction

    def set_fourier(self, fourier):
        if not isinstance(fourier, bool):
            raise ValueError('Expected fourier to be bool, found: ' + unicode(type(fourier)))
        self.fourier = fourier


class SsaForecast:

    def __init__(self, method=None, base=None):
        if method is not None:
            self.method = method
        if base is not None:
            self.base = base

    def set_method(self, method):
        if not hasattr(SsaForecastMethod, method):
            raise ValueError('Expected attribute of SsaForecastMethod, found: ' + str(method))
        self.method = method

    def set_base(self, base):
        if not hasattr(SsaForecastBase, base):
            raise ValueError('Expected attribute of SsaForecastBase, found: ' + str(base))
        self.base = base


class SsaGroup:

    def __init__(self, auto=None, manual=None):
        if auto is not None:
            self.auto = auto
        if manual is not None:
            self.manual = manual

    def set_auto(self, auto):
        if not isinstance(auto, SsaGroupAuto):
            raise ValueError('Expected SsaGroupAuto class instance, found: ' + unicode(type(auto)))
        self.auto = auto

    def set_manual(self, manual):
        if not isinstance(manual, SsaGroupManual):
            raise ValueError('Expected SsaGroupManual class instance, found: ' + unicode(type(manual)))
        self.manual = manual


class SsaGroupAuto:

    def __init__(self, count=None, stack=None, union=None, clustering=None):
        if count is not None:
            self.count = count
        if stack is not None:
            self.stack = stack
        if union is not None:
            self.union = union
        if clustering is not None:
            self.clustering = clustering

    def set_count(self, count):
        if not isinstance(count, numbers.Number):
            raise ValueError('Expected count to be a number, found: ' + unicode(type(count)))
        self.count = count

    def set_stack(self, stack):
        if not isinstance(stack, bool):
            raise ValueError('Expected stack to be bool, found: ' + unicode(type(stack)))
        self.stack = stack

    def set_union(self, union):
        if not isinstance(union, list):
            raise ValueError('Expected union to be list, found: ' + unicode(type(union)))
        self.union = union

    def set_clustering(self, clustering):
        if not isinstance(clustering, SsaGroupAutoClustering):
            raise ValueError('Expected stack to be SsaGroupAutoClustering, found: ' + unicode(type(clustering)))
        self.clustering = clustering


class SsaGroupAutoClustering:

    def __init__(self, method=None, params=None):
        if method is not None:
            self.method = method
        if params is not None:
            self.params = params

    def set_method(self, method):
        if not hasattr(SsaGroupAutoClusteringMethod, method):
            raise ValueError('Expected attribute of SsaGroupAutoClusteringMethod, found: ' + str(method))
        self.method = method

    def set_params(self, params):
        if not isinstance(params, dict):
            raise ValueError('Expected params to be a dictionary, found: ' + unicode(type(params)))
        self.params = params


class SsaGroupManual:

    def __init__(self, groups=None):
        if groups is not None:
            self.groups = groups

    def set_groups(self, groups):
        if not isinstance(groups, list):
            raise ValueError('Expected groups to be a list, found: ' + unicode(type(groups)))
        self.groups = groups


# ===============================================================================
# Properties
# ===============================================================================
class PropertiesQuery:
    """
    Class to retrieve property records for the specified parameters.
    """

    def __init__(self, entity_filter, date_filter, type, key=None, exact_match=None, key_tag_expression=None,
                 limit=None, last=None, offset=None, add_meta=None):
        copy_not_empty_attrs(entity_filter, self)
        copy_not_empty_attrs(date_filter, self)
        self.type = type
        self.key = key
        self.exactMatch = False if exact_match is None else exact_match
        self.keyTagExpression = key_tag_expression
        self.limit = 0 if limit is None else limit
        self.last = False if last is None else last
        self.offset = -1 if offset is None else offset
        self.addMeta = False if add_meta is None else add_meta

    def set_entity_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_date_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_type(self, value):
        self.type = value

    def set_key(self, value):
        self.key = value

    def set_exact_match(self, value):
        self.exactMatch = value

    def set_key_tag_expression(self, value):
        self.keyTagExpression = value

    def set_limit(self, value):
        self.limit = value

    def set_last(self, value):
        self.last = value

    def set_offset(self, value):
        self.offset = value


# ------------------------------------------------------------------------------
class PropertiesDeleteQuery:
    """
    Class to delete property records matching the specified filters.
    """

    def __init__(self, type, entity, start_date=None, end_date=None, key=None, exact_match=None):
        self.type = type
        self.entity = entity
        self.startTime = to_iso(start_date)
        self.endTime = to_iso(end_date)
        self.key = key
        self.exactMatch = False if exact_match is None else exact_match

    def set_type(self, value):
        self.type = value

    def set_entity(self, value):
        self.entity = value

    def set_start_date(self, value):
        self.startDate = to_iso(value)

    def set_end_date(self, value):
        self.endDate = to_iso(value)

    def set_key(self, value):
        self.key = value

    def set_exact_match(self, value):
        self.exactMatch = value


# ===============================================================================
# Alerts
# ===============================================================================
class AlertsQuery:
    """
    Class to retrieve open alert records for the specified filters.
    """

    def __init__(self, entity_filter, date_filter, rules=None, metrics=None, severities=None, min_severity=None,
                 acknowledged=None):
        copy_not_empty_attrs(src=entity_filter, dst=self)
        copy_not_empty_attrs(src=date_filter, dst=self)
        self.metrics = metrics
        self.rules = rules
        self.severities = severities
        self.minSeverity = min_severity
        self.acknowledged = acknowledged

    def set_entity_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_date_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_rules(self, value):
        self.rules = value

    def set_metrics(self, value):
        self.metrics = value

    def set_severities(self, value):
        self.severities = value

    def set_min_severity(self, value):
        self.minSeverity = value

    def set_acknowledged(self, value):
        self.acknowledged = value


# ------------------------------------------------------------------------------
class AlertHistoryQuery:
    """
    Class to retrieve alert history records for the specified filters.
    """

    def __init__(self, entity_filter, date_filter, rule=None, rules=None, metric=None, limit=None):
        copy_not_empty_attrs(src=entity_filter, dst=self)
        copy_not_empty_attrs(src=date_filter, dst=self)
        self.limit = limit
        self.rule = rule
        self.rules = rules
        self.metric = metric

    def set_entity_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_date_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_rule(self, value):
        self.rule = value

    def set_rules(self, value):
        self.rule = value

    def set_metric(self, value):
        self.metric = value

    def set_limit(self, value):
        self.limit = value


# ===============================================================================
# Messages
# ===============================================================================
class MessageQuery:
    """
     Class to retrieve message records for the specified filters.
    """

    def __init__(self, entity_filter, date_filter, type=None, source=None, tags=None, severity=None, severities=None,
                 min_severity=None, limit=None, expression=None):
        copy_not_empty_attrs(entity_filter, self)
        copy_not_empty_attrs(date_filter, self)
        self.type = type
        self.source = source
        self.tags = tags
        self.severity = severity
        self.severities = severities
        self.minSeverity = min_severity
        self.limit = 1000 if limit is None else limit
        self.expression = expression

    def set_entity_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_date_filter(self, value):
        copy_not_empty_attrs(value, self)

    def set_type(self, value):
        self.type = value

    def set_source(self, value):
        self.source = value

    def set_tags(self, value):
        self.tags = value

    def set_severity(self, value):
        self.severity = value

    def set_severities(self, value):
        self.severities = value

    def set_min_severity(self, value):
        self.minSeverity = value

    def set_limit(self, value):
        self.limit = value

    def set_expression(self, value):
        self.expression = value
