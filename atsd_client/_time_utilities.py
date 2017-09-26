import calendar
import numbers

import dateutil.parser
import sys
import time
from datetime import datetime
from dateutil.tz import tzlocal, tzutc

try:
    unicode = unicode
except NameError:
    unicode = str

def _current_aware_datetime():
    return datetime.now(tzlocal())

def _current_aware_timestring():
    return str(datetime.now(tzlocal()).replace(microsecond=0).isoformat())

def _iso_to_milliseconds(time_string):
    """
    :param time_string: in iso 8601 format'
    :return: timestamp in milliseconds
    """
    utc_dt = dateutil.parser.parse(time_string)
    return calendar.timegm(utc_dt.timetuple()) * 1000


def _dt_to_utc(datetime_obj):
    """
    :param datetime_obj: datetime object'
    :return: datetime instance
    """
    if datetime_obj.tzinfo is None:
        return datetime_obj.replace(tzinfo=tzlocal()).astimezone(tzutc())
    else:
        return datetime_obj.astimezone(tzutc())

def to_timestamp(time):
    """
    :param time: None | `str` in iso format | :class:`datetime` | `int`
    :return: timestamp in milliseconds
    """
    return _iso_to_milliseconds(to_iso_utc(time))

def to_iso_utc(time):
    """
    :param time: None | iso `str` | :class:`datetime` | `int`
    :return: timestamp in milliseconds
    """
    aux_time = None
    if time is None:
        aux_time = _current_aware_datetime()
    if isinstance(time, (str, unicode)):
        try:
            aux_time = dateutil.parser.parse(time)
        except ValueError:
            return time
    elif isinstance(time, datetime):
        aux_time = time
    elif isinstance(time, numbers.Number):
        aux_time = datetime.utcfromtimestamp(time * 0.001).replace(tzinfo=tzutc())  # expecting milliseconds
    elif aux_time is None:
        raise ValueError('data "time" should be either number, datetime instance, None or str')
    return str(_dt_to_utc(aux_time).replace(microsecond=0).isoformat())

def timediff_in_minutes(prev_date, next_date=None):
    """
    Return timediff in minutes.
    If first date is not specified return sys.maxsize
    If second date is not specified set it to current time.
    :param prev_date: None | iso `str` | :class:`datetime` | `int`
    :param next_date: None | iso `str` | :class:`datetime` | `int`
    :return: timediff in minutes
    """
    if prev_date is None:
        return sys.maxsize

    if isinstance(prev_date, (str, unicode)):
        try:
            prev_date = dateutil.parser.parse(prev_date)
        except ValueError:
            return prev_date
    elif isinstance(prev_date, datetime):
        prev_date = prev_date
    elif isinstance(prev_date, numbers.Number):
        prev_date = datetime.utcfromtimestamp(prev_date * 0.001).replace(tzinfo=tzutc())  # expecting milliseconds
    elif prev_date is None:
        raise ValueError('data "prev_date" should be either number, datetime instance, None or str')

    if next_date is None:
        next_date = datetime.now(tzutc())
    elif isinstance(next_date, (str, unicode)):
        try:
            next_date = dateutil.parser.parse(next_date)
        except ValueError:
            return next_date
    elif isinstance(next_date, datetime):
        next_date = next_date
    elif isinstance(next_date, numbers.Number):
        next_date = datetime.utcfromtimestamp(next_date * 0.001).replace(tzinfo=tzutc())  # expecting milliseconds
    elif next_date is None:
        raise ValueError('data "next_date" should be either number, datetime instance, None or str')

    prev_date_date_ts = time.mktime(_dt_to_utc(prev_date).timetuple())
    next_date_ts = time.mktime(_dt_to_utc(next_date).timetuple())

    return int(next_date_ts - prev_date_date_ts) / 60