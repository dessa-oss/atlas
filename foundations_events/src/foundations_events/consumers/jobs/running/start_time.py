
from foundations_events.consumers.jobs.mixins.time_setter import TimeSetter


class StartTime(TimeSetter):
    """Saves the start time of a job to redis

    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def _listing_name(self):
        return 'jobs'

    def _listing_value(self, message):
        return message['job_id']

    def _timestamp_name(self):
        return 'start_time'
