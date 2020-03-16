
from foundations_events.consumers.jobs.mixins.property_setter import PropertySetter


class JobState(PropertySetter):
    """Sets the state of a job to queued in redis

    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def _listing_name(self):
        return 'jobs'

    def _listing_value(self, message):
        return message['job_id']

    def _property_name(self):
        return 'state'

    def _property_value(self, message, timestamp, meta_data):
        return 'running'
