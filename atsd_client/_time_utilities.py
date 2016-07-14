import time
import copy
import dateutil.parser
from datetime import datetime
from dateutil.tz import tzlocal, tzutc
import numbers

def _current_milliseconds():
    return int(current_aware_datetime().timestamp() * 1000)

def _iso_to_milliseconds(time_string):
    """
    :param time_string: in iso 8601 format'
    :return: timestamp in milliseconds
    """
    utc_dt = dateutil.parser.parse(time_string)
    return utc_dt.timestamp() * 1000

def _milliseconds_to_utc_dt(ts):
    """
    :param ts: int timestamp'
    :return: UTC datetime object
    """
    return datetime.utcfromtimestamp(ts * 0.001)

def _dt_to_milliseconds(datetime_obj):
    """
    :param datetime_obj: datetime object'
    :return: timestamp in milliseconds
    """
    offset = datetime_obj.utcoffset() if datetime_obj.utcoffset() is not None else timedelta(seconds=-time.timezone)
    utc_naive = datetime_obj.replace(tzinfo=None) - offset
    return int((utc_naive - datetime(1970, 1, 1)).total_seconds() * 1000)

def _dt_to_utc(datetime_obj):
    """
    :param datetime_obj: datetime object'
    :return: datetime instance
    """
    return datetime_obj.astimezone(tzutc())

def to_timestamp(time):
    """
    :param time: None| `str` | :class: `.datetime` | `int`
    :return: timestamp in milliseconds
    """
    if time is None:
        return _current_milliseconds()
    if isinstance(time, str):
        return _iso_to_milliseconds(time)
    elif isinstance(time, datetime):
        return _dt_to_milliseconds(time)
    elif isinstance(time, numbers.Number):
        return time
    else:
        raise ValueError('data "time" should be either number, datetime instance, None or str')
