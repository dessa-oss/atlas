

class QueuedJobQuery(object):

    def __init__(self, redis, job_id):
        self._redis = redis
        self._job_id = job_id

    def queued_time(self):
        stored_value = self._redis.get('jobs:{}:creation_time'.format(self._job_id))
        return stored_value

    def project_name(self):
        stored_value = self._redis.get('jobs:{}:project'.format(self._job_id))
        return stored_value

    def exists(self):
        return self._redis.sismember('projects:global:jobs:queued', self._job_id)