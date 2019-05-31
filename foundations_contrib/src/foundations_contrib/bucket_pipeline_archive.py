"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.utils import file_archive_name
from foundations_contrib.utils import file_archive_name_with_additional_prefix


class BucketPipelineArchive(object):

    def __init__(self, bucket_constructor, *constructor_args, **constructor_kwargs):
        self._bucket = bucket_constructor(
            *constructor_args, **constructor_kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def append(self, name, item, prefix=None):
        from foundations_internal.serializer import serialize

        serialized_item = serialize(item)
        self.append_binary(name, serialized_item, prefix)

    def append_binary(self, name, serialized_item, prefix=None):
        arcname = file_archive_name(prefix, name)
        self._bucket.upload_from_string(arcname, serialized_item)

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename

        name = target_name or basename(file_path)
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)
        with open(file_path, 'rb') as file:
            self._bucket.upload_from_file(arcname, file)

    def fetch(self, name, prefix=None):
        from foundations_internal.serializer import deserialize

        serialized_item = self.fetch_binary(name, prefix)
        return deserialize(serialized_item)

    def fetch_binary(self, name, prefix=None):
        arcname = file_archive_name(prefix, name)
        if self._bucket.exists(arcname):
            return self._bucket.download_as_string(arcname)
        else:
            return None

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename

        name = file_path or target_name
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)

        if self._bucket.exists(arcname):
            with open(target_name, 'w+b') as file:
                self._bucket.download_to_file(arcname, file)
            return True

        return False
