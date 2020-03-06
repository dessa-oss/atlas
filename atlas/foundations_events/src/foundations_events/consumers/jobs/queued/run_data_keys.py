
from foundations_events.consumers.jobs.queued.mixins.attribute_key_list import AttributeKeyList


class RunDataKeys(AttributeKeyList):
    """Stores a list of all common job run data parameter keys for a project in redis

    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def _get_attribute(self, message):
        return message['job_parameters']

    def _get_attribute_key(self):
        return 'job_parameter_names'
