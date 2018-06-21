class S3Bucket(object):
    def __init__(self, bucket_name):
        import boto3
        self._bucket = boto3.resource('s3').Bucket(bucket_name)

    def upload_from_string(self, name, data):
        from vcat.utils import byte_string
        self._bucket.put_object(Key=name, Body=byte_string(data))

    def upload_from_file(self, name, input_file):
        self._bucket.upload_file(input_file, name)

    def exists(self, name):
        objs = self._objs_with_prefix(name)

        for obj in objs:
            if obj.key == name:
                return True

        return False

    def download_as_string(self, name):
        from vcat.utils import byte_string

        objs = self._objs_with_prefix(name)
        for obj in objs:
            if obj.key == name:
                return byte_string(_read_streamed_object(obj))

    def download_to_file(self, name, output_file):
        self._bucket.download_file(name, output_file)

    def list_files(self, pathname):
        from os.path import dirname
        from os.path import basename
        from fnmatch import fnmatch

        directory = dirname(pathname)
        path_filter = basename(pathname)

        objects = self._objs_with_directory(directory)
        object_names = [bucket_object.key for bucket_object in objects]
        object_file_names = [basename(path) for path in object_names]
        return filter(lambda path: fnmatch(path, path_filter), object_file_names)

        objs = self._objs_with_prefix(pathname)
        return [obj.key for obj in objs]

    def _objs_with_prefix(self, prefix):
        return self._bucket.objects.filter(Prefix=prefix)

    def _objs_with_directory(self, directory):
        return self._bucket.objects.filter(Prefix=directory + '/', Delimiter='/')

def _read_streamed_object(obj):
    return obj.get()['Body'].read()
