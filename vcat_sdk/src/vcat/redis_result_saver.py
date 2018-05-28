class RedisResultSaver(object):

    def __init__(self):
        import redis

        self._connection = redis.Redis()

    def save(self, name, results):
        import dill as pickle

        results_serialized = pickle.dumps(results)
        self._connection.sadd("result_names", name)
        self._connection.set("results:" + name, results_serialized)

    def clear(self):
        return self._connection.delete("result_names")
