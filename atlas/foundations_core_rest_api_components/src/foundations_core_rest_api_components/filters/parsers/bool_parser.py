

class BoolParser(object):

    def parse(self, value):
        return True if self._is_true(value) else False if self._is_false(value) else None

    def _is_true(self, value):
        return str(value).title() == 'True'

    def _is_false(self, value):
        return str(value).title() == 'False'
