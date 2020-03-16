
from foundations_events.consumers.jobs.queued.mixins.serialized_parameter import SerializedParameter


class ErrorData(SerializedParameter):
    """Save the parameter used when calling #run on a stage
    to redis

    Arguments:
        redis {redis.Redis} -- A Redis connection
        serializer {object} -- A serializer having a #dumps method to convert the data into a string
    """

    def _get_attribute(self, message):
        return message['error_information']

    def _get_attribute_key(self):
        return 'error_information'
