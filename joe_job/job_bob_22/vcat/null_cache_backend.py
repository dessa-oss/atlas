class NullCacheBackend(object):

    def get(self, key):
        return None

    def set(self, key, value):
        pass
