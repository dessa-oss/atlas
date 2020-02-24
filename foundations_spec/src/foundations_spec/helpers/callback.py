

class Callback(object):
    def __init__(self, function):
        self._function = function

    def evaluate(self, other_self):
        return self._function(other_self)