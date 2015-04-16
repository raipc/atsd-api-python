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


import time
from datetime import datetime, timedelta
import numbers
from .._jsonutil import Serializable


def _strp(time_str):
    """
    :param time_str: in format '%Y-%m-%dT%H:%M:%SZ%z'
    :return: timestamp in milliseconds
    """
    t, tz = time_str.split('Z')

    t = time.strptime(t, '%Y-%m-%dT%H:%M:%S')

    sig, hour, min = tz[0], tz[1:3], tz[3:5]

    tz_offset = int(sig + hour) * 60 * 60 + int(sig + min) * 60
    loc_offset = time.timezone
    offset = loc_offset - tz_offset

    timestamp = int((time.mktime(t) + offset) * 1000)

    return timestamp


def _to_posix_timestamp(dt):
    offset = dt.utcoffset() if dt.utcoffset() is not None else timedelta(seconds=-time.timezone)
    utc_naive = dt.replace(tzinfo=None) - offset
    return int((utc_naive - datetime(1970, 1, 1)).total_seconds() * 1000)


class Property(Serializable):
    def __init__(self, type, entity, tags,
                 key=None,
                 timestamp=None):
        #:`str` property type name
        self.type = type
        #:`str` entity name
        self.entity = entity
        #:`dict` containing object keys
        self.tags = tags

        #:`dict` of ``name: value`` pairs that uniquely identify
        #: the property record
        self.key = key
        #:time in Unix milliseconds
        self.timestamp = timestamp


class Series(Serializable):
    def __init__(self, entity, metric, data=None, tags=None):
        #:`str` entity name
        self.entity = entity
        #:`str` metric name
        self.metric = metric

        #an array of {'t': time, 'v': value} objects
        #use add value instead
        self._data = data
        #: `dict` of ``tag_name: tag_value`` pairs
        self.tags = tags

    def __str__(self):
        try:
            data = ['{t}\t{v}'.format(**item) for item in self._data]
            res = '\n'.join(data)
        except TypeError:
            res = ''

        for key in self.__dict__:
            if not key.startswith('_'):
                res += '\n{0}: {1}'.format(key, getattr(self, key))

        return res

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
            res.add_value(ts[dt], _to_posix_timestamp(dt))

        return res

    @property
    def data(self):
        """data getter, use ``add_value()`` method to set values

        :return: an array of {'t': time, 'v': value} objects
        """
        return self._data

    def add_value(self, v, t=None):
        """add time-value pair to series
        time could be specified either as `int` in milliseconds or as `str` in format
        ``%Y-%m-%dT%H:%M:%SZ%z`` (e.g. 2015-04-14T07:03:31Z)

        :param v: value number
        :param t: time if not specified t = current time
        """
        if t is None:
            t = int(time.time() * 1000)

        if isinstance(t, str):
            t = _strp(t)
        if not isinstance(t, numbers.Number):
            raise ValueError('data "t" should be either number or str')

        try:
            self._data.append({'v': v, 't': t})
        except AttributeError:
            self._data = [{'v': v, 't': t}]

    def values(self):
        if self._data is None:
            return []
        return [item['v'] for item in self._data]

    def times(self):
        if self._data is None:
            return []
        return [datetime.fromtimestamp(item['t'] * 0.001) for item in self._data]

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

            return plt.plot(self.values(), self.times())


class Alert(Serializable):
    def __init__(self, id,
                 rule=None,
                 entity=None,
                 metric=None,
                 lastEventTime=None,
                 openTime=None,
                 value=None,
                 message=None,
                 tags=None,
                 textValue=None,
                 severity=None,
                 repeatCount=None,
                 acknowledged=None,
                 openValue=None):
        self.id = id

        #: `str`
        self.rule = rule
        #: `str`
        self.entity = entity
        #: `str`
        self.metric = metric
        #: `long`
        self.lastEventTime = lastEventTime
        #: `long`
        self.openTime = openTime
        #: `Number`
        self.value = value
        self.message = message
        #: `dict`
        self.tags = tags
        #: `str`
        self.textValue = textValue
        #: :class:`.Severity`
        self.severity = severity
        #: `int`
        self.repeatCount = repeatCount
        #: `bool`
        self.acknowledged = acknowledged
        #: `Number`
        self.openValue = openValue


class AlertHistory(Serializable):
    def __init__(self,
                 alert=None,
                 alertDuration=None,
                 alertOpenTime=None,
                 entity=None,
                 metric=None,
                 receivedTime=None,
                 repeatCount=None,
                 rule=None,
                 ruleExpression=None,
                 ruleFilter=None,
                 schedule=None,
                 severity=None,
                 tags=None,
                 time=None,
                 type=None,
                 value=None,
                 window=None):
        self.alert = alert
        #: `number`
        self.alertDuration = alertDuration
        #: `long` milliseconds
        self.alertOpenTime = alertOpenTime
        #: `str`
        self.entity = entity
        #: `str`
        self.metric = metric
        #: `long` milliseconds
        self.receivedTime = receivedTime
        self.repeatCount = repeatCount
        self.rule = rule
        #: `str`
        self.ruleExpression = ruleExpression
        self.ruleFilter = ruleFilter
        self.schedule = schedule
        self.severity = severity
        #: `dict`
        self.tags = tags
        #: `long` milliseconds
        self.time = time
        self.type = type
        #: `Number`
        self.value = value
        self.window = window

# if __name__ == '__main__':
#     import pandas as pd
#     now = int(time.time() * 1000)
#     dt = datetime.fromtimestamp(now * 0.001)
#     print now, dt, _to_posix_timestamp(dt)
#
#     ts = pd.Series([1], index=[datetime.fromtimestamp(now * 0.001)])
#
#     res = _to_posix_timestamp(ts.index[0])
#     dt = datetime.fromtimestamp(res * 0.001)
#
#     print res, dt