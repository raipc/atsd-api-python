def copy_not_empty_attrs(src, dst):
    if src is not None and dst is not None:
        for attribute in src.__dict__:
            value = getattr(src, attribute)
            if value:
                setattr(dst, attribute, value)


class NoneDict(dict):
    def __getitem__(self, key):
        return dict.get(self, key)
