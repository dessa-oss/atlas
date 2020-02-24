
class ProjectName(object):
    """Saves the name of the project associated with the job to redis
    
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

        self._redis.set('jobs:{}:project'.format(message['job_id']), message['project_name'])
