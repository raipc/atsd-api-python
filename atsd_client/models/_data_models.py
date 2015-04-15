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


from ..exceptions import DataParseException
import time
from datetime import datetime, timedelta
import numbers


def _strp(time_str):
    """
    :param time_str: in format '%Y-%m-%dT%H:%M:%SZ%z'
    :return: timestamp in msec
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


def _getprop(model, prop):
    """
    :raises: :class:`.AttributeError` in case of no prop found
    :param model:
    :param prop: prop name
    :return: prop value
    """
    try:
        # try to get strictly used prop
        attr = model.__dict__[prop]
    except KeyError:
        # try to get private if setter/getter is used
        attr = getattr(model, '_' + prop)

    if isinstance(attr, _Model):
        return attr._serialize()
    else:
        return attr


class _Model(object):
    """
    subclass should overwrite _required_props & _allowed_props
    all props should be json serializable or :class:`._Model` instance

    when serializing non specified properties are ignored
    when desirializing all properties are saved

    props should be either public or use setter/getter in that case
       prop should be available via underscore name (e.g. _prop).
       It used to allow use implicit constructors
    """

    _required_props = ()
    _allowed_props = ()

    def __repr__(self):
        return repr(self.__dict__)

    def _serialize(self):
        """
        ignore non allowed props
        :raises: :class:`.DataParseException` if required prop is absent
        :return: json-serializable object
        """
        data = {}

        for prop in self._required_props:
            try:
                data[prop] = _getprop(self, prop)
            except AttributeError:
                raise DataParseException(prop, type(self))

        for prop in self._allowed_props:
            try:
                data[prop] = _getprop(self, prop)
            except AttributeError:
                pass

        return data


class Property(_Model):
    _allowed_props = ('key', 'timestamp')
    _required_props = ('type', 'entity', 'tags')

    def __init__(self, type, entity, tags, **kwargs):
        # tags=None in delete requests
        self.type = type
        self.entity = entity
        self.tags = tags

        for prop in Property._allowed_props:
            if prop in kwargs:
                setattr(self, prop, kwargs[prop])


class Series(_Model):
    _allowed_props = ('tags', 'type')
    _required_props = ('entity', 'metric', 'data')

    def __str__(self):
        try:
            data = ['{t}\t{v}'.format(**item) for item in self.data]
            res = '\n'.join(data)
        except TypeError:
            res = ''

        for key in self.__dict__:
            if key == 'data':
                continue
            res += '\n{0}: {1}'.format(key, getattr(self, key))

        return res

    def __init__(self, entity, metric, **kwargs):
        self.entity = entity
        self.metric = metric
        self.data = []

        for prop in kwargs:
            setattr(self, prop, kwargs[prop])

    @staticmethod
    def from_pandas_series(entity, metric, ts, **kwargs):
        """
        :param entity: str entity name
        :param metric: str metric name
        :param ts: pandas time series object
        :return: :class:`.Series` with data from pandas time series
        """
        data = []
        for dt in ts.index:
            data.append({
                't': _to_posix_timestamp(dt),
                'v': ts[dt]
            })

        return Series(entity, metric, data, **kwargs)

    def add_value(self, v, t=None):
        """add time-value pair to series
        time could be specified either as `int` in milliseconds or as `str` in format %Y-%m-%dT%H:%M:%SZ%z
        (e.g. 2015-04-14T07:03:31Z)

        :param v: value number
        :param t: time if not specified t = current_time
        """
        if t is None:
            t = int(time.time() * 1000)

        if isinstance(t, str):
            t = _strp(t)
        if not isinstance(t, numbers.Number):
            raise ValueError('data "t" should be either number or str')

        self.data.append({'v': v, 't': t})

    def values(self):
        return [item['v'] for item in self.data]

    def times(self):
        return [datetime.fromtimestamp(item['t'] * 0.001) for item in self.data]

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


class Alert(_Model):
    _allowed_props = ('rule',
                      'entity',
                      'metric',
                      'lastEventTime',
                      'openValues',
                      'openTime',
                      'value',
                      'message',
                      'tags',
                      'textValue',
                      'severity',
                      'repeatCount',
                      'acknowledged',
                      'openValue')
    _required_props = ('id',)

    def __init__(self, id, **kwargs):
        self.id = id

        for prop in kwargs:
            setattr(self, prop, kwargs[prop])


class AlertHistory(_Model):
    _allowed_props = ('alert',
                      'alertDuration',
                      'alertOpenTime',
                      'entity',
                      'metric',
                      'receivedTime',
                      'repeatCount',
                      'rule',
                      'ruleExpression',
                      'ruleFilter',
                      'schedule',
                      'severity',
                      'tags',
                      'time',
                      'type',
                      'value',
                      'window')
    _required_props = ()

    def __init__(self, **kwargs):
        for prop in kwargs:
            setattr(self, prop, kwargs[prop])

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