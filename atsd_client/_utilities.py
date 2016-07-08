import time

def copy_not_empty_attrs(src, dst):
    if src is not None and dst is not None:
        for attribute in src.__dict__:
            value = getattr(src, attribute)
            if value:
                setattr(dst, attribute, value)


def utc_to_milliseconds(time_str):
    """
    :param time_str: in format '%Y-%m-%dT%H:%M:%SZ%z'
    :return: timestamp in milliseconds
    """
    time_part, timezone_part = time_str.split('Z')
    time_part = time.strptime(time_part, '%Y-%m-%dT%H:%M:%S')
    if timezone_part:
        sig, hour, min = timezone_part[0], timezone_part[1:3], timezone_part[3:5]
        tz_offset = int(sig + hour) * 60 * 60 + int(sig + min) * 60
        loc_offset = time.timezone
        offset = loc_offset - tz_offset
        return int((time.mktime(time_part) + offset) * 1000)
    else:
        return int(time.mktime(time_part)) * 1000


def to_posix_timestamp(datetime_obj):
    offset = datetime_obj.utcoffset() if datetime_obj.utcoffset() is not None else timedelta(seconds=-time.timezone)
    utc_naive = datetime_obj.replace(tzinfo=None) - offset
    return int((utc_naive - datetime(1970, 1, 1)).total_seconds() * 1000)

