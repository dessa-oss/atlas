

class ProjectMetrics(object):
    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        from foundations_internal.fast_serializer import serialize

        project_key = f'projects:{message["project_name"]}:metrics'
        metric_key = f'{message["job_id"]}:{message["key"]}'
        value = (timestamp, message['value'])

        self._redis.hset(project_key, metric_key, serialize(value))
