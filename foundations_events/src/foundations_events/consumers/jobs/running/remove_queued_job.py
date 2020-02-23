
class RemoveQueuedJob(object):
    """Removes the job from a list of queued jobs for a project in redis
    
    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """
    
    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        """See above
        
        Arguments:
            message {dict} -- Event attributes
            timestamp {int} -- The time the event was created
            meta_data {dict} -- Additional data about the event
        """

        self._redis.srem('project:{}:jobs:queued'.format(message['project_name']), message['job_id'])
