

class ConnectionManager(object):

    def __init__(self):
        self._bucket_connection = None

    def bucket_connection(self):
        if self._bucket_connection is None:
            self._load()

        return self._bucket_connection

    def _load(self):
        import boto3
        self._bucket_connection = boto3.client('s3')
