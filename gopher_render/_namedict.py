"""
Custom dict class that allows values to be accessed as attributes.
"""


class namedict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if hasattr(self, name) and not name in self:
            object.__setattr__(self, name, value)
        else:
            self[name] = value

    def __delattr__(self, name):
        if hasattr(self, name) and not name in self:
            object.__delattr__(self, name)
        else:
            try:
                del self[name]
            except KeyError:
                raise AttributeError(name)
