
from foundations_events.consumers.jobs.mixins.property_setter import PropertySetter


class TimeSetter(PropertySetter):
    """Saves an event timestamp to a value in redis

    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def _timestamp_name(self):
        pass

    def _property_name(self):
        return self._timestamp_name()

    def _property_value(self, message, timestamp, meta_data):
        return str(timestamp)
