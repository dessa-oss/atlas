class ConnectionManager(object):

    def __init__(self):
        self._bucket_connection = None

    def bucket_connection(self):
        if self._bucket_connection is None:
            self._load()

        return self._bucket_connection

    def _load(self):
        from google.cloud.storage import Client
        self._bucket_connection = Client()
