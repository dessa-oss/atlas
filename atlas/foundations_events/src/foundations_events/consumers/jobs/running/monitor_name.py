
class MonitorName(object):
    """Saves the name of the monitor associated with the job to redis
    
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
        job_id = message['job_id']
        monitor_name = message['monitor_name']
        project_name = message['project_name']
        self._redis.sadd(f'projects:{project_name}:monitors:{monitor_name}:jobs', job_id)
