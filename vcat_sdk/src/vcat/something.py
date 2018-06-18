class Something(object):

    def __init__(self, value):
        self._value = value

    def map(self, function):
        return Something(function(self._value))

    def is_present(self):
        return True

    def get(self):
        return self._value

    def get_or_else(self, value):
        return self.get()

    def fallback(self, callback):
        return self

    def __eq__(self, other):
        if isinstance(other, Something):
            return self._value == other._value
        else:
            return False