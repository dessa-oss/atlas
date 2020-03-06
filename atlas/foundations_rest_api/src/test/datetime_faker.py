import datetime
import time


class _DateTimeHolder(object):
    _python_datetime = None
    _python_time = None


def fake_current_datetime(fake_timestamp):

    class FakeDateTime(datetime.datetime):
        @staticmethod
        def now():
            return FakeDateTime.utcfromtimestamp(fake_timestamp)

    def fake_time():
        return fake_timestamp

    if not (_DateTimeHolder._python_datetime and _DateTimeHolder._python_time):
        _DateTimeHolder._python_datetime = datetime.datetime
        _DateTimeHolder._python_time = time.time

    datetime.datetime = FakeDateTime
    time.time = fake_time


def restore_real_current_datetime():
    if _DateTimeHolder._python_datetime and _DateTimeHolder._python_time:
        datetime.datetime = _DateTimeHolder._python_datetime
        time.time = _DateTimeHolder._python_time
    else:
        raise ValueError('Could not re-establish python real current time value')
