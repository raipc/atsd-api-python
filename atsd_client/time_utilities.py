import time
import dateutil.parser
from datetime import datetime
from dateutil.tz import tzlocal, tzutc

def current_aware_time():
    return datetime.now(tzlocal())

def current_aware_timestring():
    return str(datetime.now(tzlocal()).replace(microsecond=0).isoformat())

def iso_to_milliseconds(time_string):
    """
    :param time_string: in iso 8601 format'
    :return: timestamp in milliseconds
    """
    utc_dt = dateutil.parser.parse(time_string)
    return utc_dt.timestamp() * 1000

def milliseconds_to_utc(ts):
    return datetime.utcfromtimestamp(ts * 0.001)

def dt_to_milliseconds(datetime_obj):
    """
    :param datetime instance'
    :return: timestamp in milliseconds
    """
    offset = datetime_obj.utcoffset() if datetime_obj.utcoffset() is not None else timedelta(seconds=-time.timezone)
    utc_naive = datetime_obj.replace(tzinfo=None) - offset
    return int((utc_naive - datetime(1970, 1, 1)).total_seconds() * 1000)

def dt_to_utc(dt_obj):
    return dt_obj.astimezone(tzutc())
