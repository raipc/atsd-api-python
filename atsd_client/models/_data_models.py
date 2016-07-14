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
import copy
from _constants import display_series_threshold, display_series_part, utc_format

from datetime import datetime, timedelta
from .._time_utilities import to_timestamp, _milliseconds_to_utc_dt

class Sample():
    """
        Class that represents a numeric value observed at some time with additional version information if provided.
        :param value: value of sample
        :param time: time of sample. time could be specified as `int` in milliseconds, as `str` in format ``%Y-%m-%dT%H:%M:%SZ%z`` (e.g. 2015-04-14T07:03:31Z), as `datetime`
        :param version: `dict`
    """
    
    def __repr__(self):
        return "<{v}@{t}({vv})>".format(v=self.v, t=self.t, vv=self.version)
    
    def __init__(self, value, time=None, version=None):
        self.v = copy.deepcopy(value) if not value == "Nan" else float("nan") 
        self.t = to_timestamp(time)
        self.version = version
        
        
    def compare(self, other):
            return self.t - other.t

    def __lt__(self, other):
        return self.compare(other) < 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __ne__(self, other):
        return self.compare(other) != 0
  

#------------------------------------------------------------------------------ 
class Series():
    def __init__(self, entity, metric, data=None, tags=None):
        self.entity = entity
        self.metric = metric
        self.tags = tags
        self.data = []
        self.data = []
        if data is not None:
            for data_unit in data:
                if isinstance(data_unit, dict): #Compatability
                    self.data.append(Sample(
                                            value=data_unit['v'],
                                            time=data_unit.get('t', data_unit.get('d', None)), 
                                            version=data_unit.get('version', None)
                                            )
                                    )
                else:
                    self.data.append(data_unit)
    
    def add_samples(self, *samples):
        """
        add sample to series
        """
        for sample in samples:
            self.data.append(sample)
        
    def __repr__(self):
        if len(self.data) > display_series_threshold:
            displayed_data = self.data[:display_series_part] + self.data[-display_series_part:]
        else:
            displayed_data = self.data
        rows = []
        versioned = False
        for sample in sorted(displayed_data):
            time = sample.t
            value = sample.v
            row = '{0}{1: >14}'.format(time, value)
            if sample.version is not None:
                versioned = True
                source = sample.version.get('source', '')
                status = sample.version.get('status', '')
                row += '{0: >17}{1: >17}'.format(source, status)
            rows.append(row)
        if versioned:
            header = ('           time'
                      '         value'
                      '   version_source'
                      '   version_status'
                      )
            rows.insert(0, header)
        if len(self.data) > 20:
            result = '\n'.join(rows[:-display_series_part]) + '\n...\n' + '\n'.join(rows[-display_series_part:])
        else:
            result = '\n'.join(rows)
        for attr_name in self.__dict__:
            if not attr_name.startswith('_'):
                result += '\n{0}: {1}'.format(attr_name, getattr(self, attr_name))
        return result

    def sort(self, key=None, reverse=False):
        """
        Sort series data in place
        :param key:
        :param reverse:
        """
        self.data.sort(key=key, reverse=reverse)
    
    def values(self):
        """valid versions of series values
        :return: list of `Number`
        """
        data = sorted(self.data)
        result = []
        for num, sample in enumerate(data):
            if num > 0 and sample.t == data[num - 1].t:
                result.pop()
            result.append(sample.v)
        return result

    def times(self):
        """
        valid versions of series times in seconds
        :return: list of `float`
        """
        data = sorted(self.data)
        result = []
        for num, sample in enumerate(data):
            if num > 0 and sample.t == data[num - 1].t:
                result.pop()
            new_time = _milliseconds_to_utc_dt(sample.t)
            result.append(new_time)
        return result

    @staticmethod
    def from_pandas_series(entity, metric, ts):
        """
        :param entity: str entity name
        :param metric: str metric name
        :param ts: pandas time series object
        :return: :class:`.Series` with data from pandas time series
        """
        res = Series(entity, metric)
        for dt in ts.index:
            res.add_sample(ts[dt], dt)
        return res

    def to_pandas_series(self):
        """
        :return: pandas time series object
        """
        import pandas as pd
        return pd.Series(self.values(), index=self.times())

    def plot(self):
        """
        plot series in matplotlib.pyplot
        """
        try:
            return self.to_pandas_series().plot()
        except ImportError:
            import matplotlib.pyplot as plt
            p = plt.plot(self.times(), self.values())
            plt.show(p)

#------------------------------------------------------------------------------ 
class Property():
    def __repr__(self):
            return "<PROPERTY type={type}, entity={entity}, tags={tags}...>".format(type=self.type, entity=self.entity, tags=self.tags)
        
    def __init__(self, type, entity, tags, key=None, date=None):
        """
        :param type: str  Property type name 
        :param entity: str  Entity name
        :param tags: dict Object containing name=value fields that are not part of the key and contain descriptive information about the property record. 
        :param key: dict  Object containing name=value fields that uniquely identify the property record. 
        :param date: str  ISO 8601 date, for example 2016-05-25T00:15:00Z. Set to server time at server side if omitted.
        """
        self.type = type
        self.entity = entity
        self.tags = tags
        self.key = key
        self.date = date
        
#------------------------------------------------------------------------------ 
class Alert():
    def __repr__(self):
            return "<ALERT id={id}, text={text}, entity={entity}, metric={metric}, openDate={openDate}...>".format(id=self.id, entity=self.entity, metric=self.metric, openDate=self.openDate, text=self.textValue)
    #Checked
    def __init__(self, id, rule=None, entity=None, metric=None, lastEventDate=None, openDate=None, value=None, message=None, tags=None, textValue=None, severity=None, repeatCount=None, acknowledged=None, openValue=None):
        self.id = id
        self.rule = rule
        self.entity = entity
        self.metric = metric
        self.lastEventDate = lastEventDate
        self.openDate = openDate
        self.value = value
        self.message = message
        self.tags = tags
        self.textValue = textValue
        self.severity = severity
        self.repeatCount = repeatCount
        self.acknowledged = acknowledged
        self.openValue = openValue
        
#------------------------------------------------------------------------------ 
class AlertHistory():
    def __repr__(self):
            return "<ALERT_HISTORY alert={alert}, metric={metric}, entity={entity}, date={date}, alertOpenDate={alertOpenDate}...>".format(alert=self.alert, entity=self.entity, metric=self.metric, alertOpenDate=self.alertOpenDate, date=self.date)
        
    #Checked
    def __init__(self, alert=None, alertDuration=None, alertOpenDate=None, entity=None, metric=None, receivedDate=None, repeatCount=None, rule=None, ruleExpression=None, ruleFilter=None, schedule=None, severity=None, tags=None, time=None, type=None, date=None, value=None, window=None):
        self.alert = alert
        self.alertDuration = alertDuration
        self.alertOpenDate = alertOpenDate
        self.entity = entity
        self.metric = metric
        self.receivedDate = receivedDate
        self.repeatCount = repeatCount
        self.rule = rule
        self.ruleExpression = ruleExpression
        self.ruleFilter = ruleFilter
        self.schedule = schedule
        self.severity = severity
        self.tags = tags
        self.time = time
        self.type = type
        self.date = date
        self.value = value
        self.window = window
        
#------------------------------------------------------------------------------ 
class Message():
    def __repr__(self):
            return "<MESSAGE type={type}, source={source}, entity={entity}, date={date}...>".format(type=self.type, entity=self.entity, source=self.source, date=self.date)
            
    def __init__(self, type, source, entity, date, severity, tags, message, persist=True):
        self.type=type
        self.source=source
        self.entity=entity
        self.date=date
        self.severity=severity
        self.tags=tags
        self.message=message
        self.persist=persist
