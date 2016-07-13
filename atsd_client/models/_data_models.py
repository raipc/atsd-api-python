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
from .._time_utilities import iso_to_milliseconds, dt_to_milliseconds 

class Sample():
    """
        Class that represents a numeric value observed at some time with additional version information if provided.
        :param value: value of sample
        :param time: time of sample. time could be specified as `int` in milliseconds, as `str` in format ``%Y-%m-%dT%H:%M:%SZ%z`` (e.g. 2015-04-14T07:03:31Z), as `datetime`
        :param version: `dict`
    """
    
    def __repr__(self):
        return "<{v}-{t}--{vv}>".format(v=self.v, t=self.t, vv=self.version)
    
    def __init__(self, value, time=None, version=None):
        self.v = copy.deepcopy(value) if not value == "Nan" else float("nan") 
        self.version = version
        time_to_set = copy.deepcopy(time)
        if time is None:
            time_to_set = int(time.time() * 1000)
        elif isinstance(time, str):
            time_to_set = iso_to_milliseconds(time_to_set)
        elif isinstance(time, datetime):
            time_to_set = dt_to_milliseconds(time_to_set)
        else:
            raise ValueError('data "time" should be either number or str')
        self.t = time_to_set
        
    @staticmethod
    def compare(first, second):
        if first['t'] == second['t']:
            if ('version' not in first or 't' not in first['version']  or 'version' not in second or 't' not in second['version']):
                return 0
            else:
                return first['version']['t'] - second['version']['t']
        else:
            return first['t'] - second['t']

    def __lt__(self, other):
        return SeriesVersionKey.compare(self, other) < 0

    def __gt__(self, other):
        return SeriesVersionKey.compare(self, other) > 0

    def __eq__(self, other):
        return SeriesVersionKey.compare(self, other) == 0

    def __le__(self, other):
        return SeriesVersionKey.compare(self, other) <= 0

    def __ge__(self, other):
        return SeriesVersionKey.compare(self, other) >= 0

    def __ne__(self, other):
        return SeriesVersionKey.compare(self, other) != 0
  

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
                if isinstance(data_unit, dict):
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
        for sample in displayed_data:
            #print(sample)
            time = sample.t
            value = sample.v
            row = '{0}{1: >14}'.format(time, value)
            if sample.version is not None:
                versioned = True
                source = sample.version.get('source', '')
                status = sample.version.get('status', '')
                version_time = datetime.utcfromtimestamp(sample.version['t'] * 0.001).strftime(utc_format) if 't' in sample.version else ''
                row += '{0: >17}{1: >17}{2: >21}'.format(source, status, version_time)
            rows.append(row)
        if versioned:
            header = ('           date'
                      '         value'
                      '   version_source'
                      '   version_status'
                      '         version_time')
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
    
    #REFACTOR
    def values(self):
        """valid versions of series values
        :return: list of `Number`
        """
        data = sorted(self.data)
        result = []
        for num, sample in enumerate(data):
            if num > 0 and sample['t'] == data[num - 1]['t']:
                result[-1] = sample['v']
            else:
                result.append(sample['v'])
        return result

    #REFACTOR
    def times(self):
        """valid versions of series times in seconds
        :return: list of `float`
        """
        data = sorted(self.data)
        result = []
        for num, sample in enumerate(data):
            if num > 0 and sample['t'] == data[num - 1]['t']:
                result[-1] = datetime.utcfromtimestamp(sample['t'] * 0.001)
            else:
                result.append(datetime.utcfromtimestamp(sample['t'] * 0.001))
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
            return plt.plot(self.times(), self.values())

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
    def __init__(self, id, rule=None, entity=None, metric=None, lastEventTime=None, openTime=None, value=None, message=None, tags=None, textValue=None, severity=None, repeatCount=None, acknowledged=None, openValue=None):
        self.id = id
        self.rule = rule
        self.entity = entity
        self.metric = metric
        self.lastEventTime = lastEventTime
        self.openTime = openTime
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
    def __init__(self, alert=None, alertDuration=None, alertOpenTime=None, entity=None, metric=None, receivedTime=None, repeatCount=None, rule=None, ruleExpression=None, ruleFilter=None, schedule=None, severity=None, tags=None, time=None, type=None, value=None, window=None):
        self.alert = alert
        self.alertDuration = alertDuration
        self.alertOpenTime = alertOpenTime
        self.entity = entity
        self.metric = metric
        self.receivedTime = receivedTime
        self.repeatCount = repeatCount
        self.rule = rule
        self.ruleExpression = ruleExpression
        self.ruleFilter = ruleFilter
        self.schedule = schedule
        self.severity = severity
        self.tags = tags
        self.time = time
        self.type = type
        self.value = value
        self.window = window
        
#------------------------------------------------------------------------------ 
class Message():
    def __init__(self, type, source, entity, date, severity, tags, message, persist=True):
        self.type=type
        self.source=source
        self.entity=entity
        self.date=date
        self.severity=severity
        self.tags=tags
        self.message=message
        self.persist=persist


# if __name__ == '__main__':
#     import pandas as pd
#     now = int(time.time() * 1000)
#     dt = datetime.fromtimestamp(now * 0.001)
#     print now, dt, _dt_to_milliseconds(dt)
#     ts = pd.Series([1], index=[datetime.fromtimestamp(now * 0.001)])
#     res = _dt_to_milliseconds(ts.index[0])
#     dt = datetime.fromtimestamp(res * 0.001)
#     print res, dt