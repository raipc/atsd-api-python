def copy_not_empty_attrs(src, dst):
    for attribute in src.__dict__:
        value = getattr(src, attribute)
        if value:
            setattr(dst, attribute, value)
