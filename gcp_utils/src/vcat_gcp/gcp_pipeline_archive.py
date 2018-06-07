from vcat.utils import file_archive_name
from vcat.utils import file_archive_name_with_additional_prefix


class GCPPipelineArchive(object):

    def __init__(self, bucket):
        from vcat_gcp.gcp_bucket import GCPBucket
        from vcat.bucket_pipeline_archive import BucketPipelineArchive

        self._archive =  BucketPipelineArchive(GCPBucket, bucket)

    def __enter__(self):
        return self._archive.__enter__()

    def __exit__(self, exception_type, exception_value, traceback):
        return self._archive.__exit__(exception_type, exception_value, traceback)

    def append(self, name, item, prefix=None):
        return self._archive.append(name, item, prefix)

    def append_binary(self, name, serialized_item, prefix=None):
        return self._archive.append_binary(name, serialized_item, prefix)

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        return self._archive.append_file(file_prefix, file_path, prefix, target_name)

    def fetch(self, name, prefix=None):
        return self._archive.fetch(name, prefix)

    def fetch_binary(self, name, prefix=None):
        return self._archive.fetch_binary(name, prefix)

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        return self._archive.fetch_to_file(file_prefix, file_path, prefix, target_name)
