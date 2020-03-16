
from foundations_events.consumers.jobs.mixins.time_setter import TimeSetter


class CreationTime(TimeSetter):
    """Stores the creation time for a queued job

    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def _listing_name(self):
        return 'jobs'

    def _listing_value(self, message):
        return message['job_id']

    def _timestamp_name(self):
        return 'creation_time'
