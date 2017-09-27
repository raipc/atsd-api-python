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
from .._time_utilities import to_iso_utc

#------------------------------------------------------------------------------ 
class DataType(object):
    SHORT    = 'SHORT'
    INTEGER  = 'INTEGER'
    FLOAT    = 'FLOAT'
    LONG     = 'LONG'
    DOUBLE   = 'DOUBLE'

#------------------------------------------------------------------------------ 
class TimePrecision(object):
    SECONDS      = 'SECONDS'
    MILLISECONDS = 'MILLISECONDS'

#------------------------------------------------------------------------------ 
class InvalidAction(object):
    NONE      = 'NONE'
    DISCARD   = 'DISCARD'
    TRANSFORM = 'TRANSFORM'
    RAISE_ERROR   = 'RAISE_ERROR'
    TRANSFORM = 'SET_VERSION_STATUS'

#------------------------------------------------------------------------------ 
class Metric():
    """
    Class representing a single metric.
    Metrics are names assigned to numeric measurements, for example, temperature or speed.
    A time-indexed array of measurements for a given entity and metric is called a time-series (or simply series).
    Metrics specify how incoming data should be stored (data type), validated and pruned.
    In addition, metrics can have user-defined tags such as unit of measurement, scale, type or a category that can be used for filtering and grouping.
    """
    
    def __init__(self,
                 name,
                 label=None,
                 enabled=None,
                 dataType=None,
                 timePrecision=None,
                 persistent=None,
                 filter=None,
                 minValue=None,
                 maxValue=None,
                 invalidAction=None,
                 description=None,
                 retentionDays=None,
                 seriesRetentionDays=None,
                 lastInsertDate=None,
                 tags=None,
                 versioned=None,
                 interpolate=None,
                 units=None,
                 timeZone=None
                 ):
        #: `str` metric name
        self.name = name
        #: `str`
        self.label = label
        #: `bool`
        self.enabled = enabled
        #: :class:`.DataType`
        self.dataType = dataType
        #: :class:`.TimePrecision`
        self.timePrecision = timePrecision
        #: `bool` persistence status. Non-persistent metrics are not stored in the database and are only processed by the rule engine
        self.persistent = persistent
        #: If filter is specified, metric puts that do not match the filter are discarded
        self.filter = filter
        #: `Number` minimum value for Invalid Action trigger
        self.minValue = minValue
        #: `Number` maximum value for Invalid Action trigger
        self.maxValue = maxValue
        #: :class:`.InvalidAction`
        self.invalidAction = invalidAction
        #: `str` metric description
        self.description = description
        #: `Number` number of days to store the values for this metric in the database
        self.retentionDays = retentionDays
        #: `Number` number of days to retain series in the database
        self.seriesRetentionDays = seriesRetentionDays
        #: :class:`datetime` object | `long` milliseconds | `str` ISO 8601 date. Last time a value was received for this metric by any series
        self.lastInsertDate = None if lastInsertDate is None else to_iso_utc(lastInsertDate)
        #: `dict`
        self.tags = tags
        #: `boolean` If set to true, enables versioning for the specified metric. When metrics is versioned, the database retains the history of series value changes for the same timestamp along with version_source and version_status 
        self.versioned = versioned
        #: :class:`.Interpolate`
        self.interpolate = interpolate
        #: `str` metric units
        self.units = units
        #: `str` entity timezone
        self.timeZone = timeZone

    def __repr__(self):
        return "<METRIC name={name}, label={label}, description={des}".format(name=self.name, label=self.label, des=self.description)
    
    #Getters and setters
    @property
    def name(self):
        return self.name

    @property
    def label(self):
        return self.label

    @property
    def enabled(self):
        return self.enabled

    @property
    def dataType(self):
        return self.dataType

    @property
    def timePrecision(self):
        return self.timePrecision

    @property
    def persistent(self):
        return self.persistent

    @property
    def filter(self):
        return self.filter

    @property
    def minValue(self):
        return self.minValue

    @property
    def maxValue(self):
        return self.maxValue

    @property
    def invalidAction(self):
        return self.invalidAction

    @property
    def description(self):
        return self.description

    @property
    def retentionDays(self):
        return self.retentionDays

    @property
    def seriesRetentionDays(self):
        return self.seriesRetentionDays

    @property
    def lastInsertDate(self):
        return self.lastInsertDate

    @property
    def tags(self):
        return self.tags

    @property
    def versioned(self):
        return self.versioned

    @property
    def interpolate(self):
        return self.interpolate

    @property
    def units(self):
        return self.units

    @property
    def timeZone(self):
        return self.timeZone

    @name.setter
    def name(self, value):
        self.name = value

    @label.setter
    def label(self, value):
        self.label = value

    @enabled.setter
    def enabled(self, value):
        self.enabled = value

    @dataType.setter
    def dataType(self, value):
        self.dataType = value

    @timePrecision.setter
    def timePrecision(self, value):
        self.timePrecision = value

    @persistent.setter
    def persistent(self, value):
        self.persistent = value

    @filter.setter
    def filter(self, value):
        self.filter = value

    @minValue.setter
    def minValue(self, value):
        self.minValue = value

    @maxValue.setter
    def maxValue(self, value):
        self.maxValue = value

    @invalidAction.setter
    def invalidAction(self, value):
        self.invalidAction = value

    @description.setter
    def description(self, value):
        self.description = value

    @retentionDays.setter
    def retentionDays(self, value):
        self.retentionDays = value

    @seriesRetentionDays.setter
    def seriesRetentionDays(self, value):
        self.seriesRetentionDays = value

    @lastInsertDate.setter
    def lastInsertDate(self, value):
        self.lastInsertDate = None if value is None else to_iso_utc(value)

    @tags.setter
    def tags(self, value):
        self.tags = value

    @versioned.setter
    def versioned(self, value):
        self.versioned = value

    @interpolate.setter
    def interpolate(self, value):
        self.interpolate = value

    @units.setter
    def units(self, value):
        self.units = value

    @timeZone.setter
    def timeZone(self, value):
        self.timeZone = value

#------------------------------------------------------------------------------ 
class Entity():
    """
    Class representing a single entitiy.
    Entities are servers, hosts, frames, virtual machines, sensors, etc.
    Entities are ingested with attached metrics (time series data) using the csv/nmon parsers, telnet and http/s protocols, and Axibase Collector jobs.
    """
    
    def __init__(self, name, enabled=None, label=None, interpolate=None, timeZone=None, lastInsertDate=None, tags=None):
        #: `str` entity name
        self.name = name
        #: `str` entity label
        self.label = label
        #: :class:`.Interpolate`
        self.interpolate = interpolate
        #: `str` entity timezone
        self.timeZone = timeZone
        #: `bool` enabled status. Incoming data is discarded for disabled entities
        self.enabled = enabled
        #: :class:`datetime` object | `long` milliseconds | `str` ISO 8601 date. Last time when a value was received by the database for this entity
        self.lastInsertDate = None if lastInsertDate is None else to_iso_utc(lastInsertDate)
        #: `dict`
        self.tags = tags
        
    def __repr__(self):
        return "<Entity name={name}, label={label}, interpolate={interpolate}, timezone={timezone}, enabled={" \
               "enabled}, lastInsertDate={lit}, tags={tags}".format(name=self.name, label=self.label,
                                                                    interpolate=self.interpolate,
                                                                    timezone=self.timeZone, enabled=self.enabled,
                                                                    lit=self.lastInsertDate, tags=self.tags)

    #Getters and setters
    @property
    def name(self):
        return self.name

    @property
    def label(self):
        return self.label

    @property
    def interpolate(self):
        return self.interpolate

    @property
    def timeZone(self):
        return self.timeZone

    @property
    def enabled(self):
        return self.enabled

    @property
    def lastInsertDate(self):
        return self.lastInsertDate

    @property
    def tags(self):
        return self.tags

    @name.setter
    def name(self, value):
        self.name = value

    @label.setter
    def label(self, value):
        self.label = value

    @interpolate.setter
    def interpolate(self, value):
        self.interpolate = value

    @timeZone.setter
    def timeZone(self, value):
        self.timeZone = value

    @enabled.setter
    def enabled(self, value):
        self.enabled = value

    @lastInsertDate.setter
    def lastInsertDate(self, value):
        self.lastInsertDate = None if value is None else to_iso_utc(value)

    @tags.setter
    def tags(self, value):
        self.tags = value

#------------------------------------------------------------------------------ 
class EntityGroup():
    """
    Class representing a single entity group.
    Entities can be grouped into Entity Groups which can be used for building Portals, Exporting Data, and creating Forecasts.
    Forecasts can be calculated for all entities present in the group.
    Data or Forecasts can be exported for all entities present in the group.
    Portals can be added to all entities present in the Group.
    This is a useful feature when working with large amounts of entities and big data sets.
    """
    def __init__(self, name, expression=None, tags=None, enabled=None):
        #: `str` entity group name
        self.name = name
        #: `str` group membership expression. The expression is applied to entities to automatically add/remove members of this group
        self.expression = expression
        #: `dict`
        self.tags = tags
        #: `bool`
        self.enabled = enabled
    
    def __repr__(self):
        return "<EntityGroup name={name}, expression={expression}, tags={tags}>".format(name=self.name, expression=self.expression, tags=self.tags, enabled=self.enabled)
    
    #Getters and setters
    @property
    def name(self):
        return self.name

    @property
    def expression(self):
        return self.expression

    @property
    def tags(self):
        return self.tags

    @property
    def enabled(self):
        return self.enabled

    @name.setter
    def name(self, value):
        self.name = value

    @expression.setter
    def expression(self, value):
        self.expression = value

    @tags.setter
    def tags(self, value):
        self.tags = value

    @enabled.setter
    def enabled(self, value):
        self.enabled = value
