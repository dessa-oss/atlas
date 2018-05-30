class NullCache(object):

    def get(self, key):
        return None

    def set(self, key, value):
        return value

    def get_or_set(self, key, value):
        return value

    def get_or_set_callback(self, key, callback):
        return callback()
