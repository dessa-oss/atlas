class GCPCacheBackend(object):

    def __init__(self, bucket):
        from vcat_gcp.gcp_bucket import GCPBucket

        self._bucket = GCPBucket(bucket)

    def get(self, key):
        import dill as pickle

        if self._bucket.exists(key):
            return pickle.loads(self._bucket.download_as_string(key))

    def set(self, key, value):
        import dill as pickle

        serialized_value = pickle.dumps(value, protocol=2)
        self._bucket.upload_from_string(key, serialized_value)
