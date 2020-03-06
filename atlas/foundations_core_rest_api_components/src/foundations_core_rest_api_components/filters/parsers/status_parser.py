
class StatusParser(object):

    _valid_statuses = ['QUEUED', 'RUNNING', 'COMPLETED', 'FAILED']

    def parse(self, value):
        value = str(value).upper()
        if value not in self._valid_statuses:
            return None
        return value
