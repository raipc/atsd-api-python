import six


def print_tags(tags):
    return ';'.join(['%s=%s' % (k, v) for k, v in six.iteritems(tags)])
