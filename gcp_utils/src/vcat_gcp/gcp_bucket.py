class GCPBucket(object):

    def __init__(self, name):
        from google.cloud.storage import Client

        self._connection = Client()
        self._result_bucket_connection = self._connection.get_bucket(name)

    def upload_from_string(self, name, data):
        pass

    def upload_from_file(self, name, input_file):
        pass

    def exists(self, name):
        pass

    def download_as_string(self, name):
        pass

    def download_to_file(self, name, output_file):
        pass

    def list_files(self, pathname):
        from os.path import dirname
        from os.path import basename
        from fnmatch import fnmatch

        directory = dirname(pathname)
        path_filter = basename(pathname)

        objects = self._result_bucket_connection.list_blobs(
            prefix=directory + '/', delimiter='/')
        object_names = [bucket_object.name for bucket_object in objects]
        object_file_names = [basename(path) for path in object_names]
        return filter(lambda path: fnmatch(path, path_filter), object_file_names)
