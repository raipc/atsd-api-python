import time
import dateutil.parser
from ._constants import utc_format

def copy_not_empty_attrs(src, dst):
    if src is not None and dst is not None:
        for attribute in src.__dict__:
            value = getattr(src, attribute)
            if value:
                setattr(dst, attribute, value)


def utc_to_milliseconds(time_string):
    """
    :param time_string: in iso 8601 format'
    :return: timestamp in milliseconds
    """
    dt = dateutil.parser.parse(time_string)
    return dt.timestamp()


def to_posix_timestamp(datetime_obj):
    offset = datetime_obj.utcoffset() if datetime_obj.utcoffset() is not None else timedelta(seconds=-time.timezone)
    utc_naive = datetime_obj.replace(tzinfo=None) - offset
    return int((utc_naive - datetime(1970, 1, 1)).total_seconds() * 1000)

