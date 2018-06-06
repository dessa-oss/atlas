class BucketPipelineListing(object):

    def __init__(self, bucket_constructor, constructor_arguments):
        self._bucket = bucket_constructor(constructor_arguments)

    def track_pipeline(self, pipeline_name):
        self._bucket.upload_from_string(pipeline_name + '.tracker', pipeline_name)

    def get_pipeline_names(self):
        file_names = self._bucket.list_files('*.tracker')
        return [self._bucket.download_as_string(name) for name in file_names]