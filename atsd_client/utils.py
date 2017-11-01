import six


def pretty_print_dict(tags):
    return ';'.join(['%s=%s' % (k, v) for k, v in six.iteritems(tags)])
