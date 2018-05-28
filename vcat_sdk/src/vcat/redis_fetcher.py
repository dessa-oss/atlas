class RedisFetcher(object):

    def __init__(self):
        import redis

        self._connection = redis.Redis()

    def fetch_results(self):
        import pickle

        result_names = self._connection.smembers("result_names")
        result_keys = ["results:" +
                       name.decode("utf-8") for name in result_names]
        results_serialized = [self._connection.get(key) for key in result_keys]
        return [pickle.loads(result_serialized) for result_serialized in results_serialized]
