class Cache(object):

    def __init__(self, cache_backend):
        self._cache_backend = cache_backend

    def get(self, key):
        return self._cache_backend.get(key)

    def set(self, key, value):
        self._cache_backend.set(key, value)
        return value

    def get_or_set(self, key, value):
        return self.get(key) or self.set(key, value)

    def get_or_set_callback(self, key, callback):
        return self.get(key) or self.set(key, callback())
