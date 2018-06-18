class GCPCacheBackend(object):

    def __init__(self, bucket):
        from vcat_gcp.gcp_bucket import GCPBucket

        self._bucket = GCPBucket(bucket)

    def get(self, key):
        if self._bucket.exists(key):
            return self._bucket.download_as_string(key)

    def set(self, key, serialized_value):
        self._bucket.upload_from_string(key, serialized_value)
