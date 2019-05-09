"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def data_from_file(file_name_with_scheme):
    from foundations_internal.serializer import deserialize

    absolute_file_path = _absolute_path_to_local_file(file_name_with_scheme)
    serialized_data_from_file = _file_data_from_local_storage(absolute_file_path)
    return deserialize(serialized_data_from_file)

def _absolute_path_to_local_file(file_name_with_scheme):
    from urllib.parse import urlparse
    return urlparse(file_name_with_scheme).path

def _file_data_from_local_storage(absolute_path):
    from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

    file_name = _file_name_from_absolute_path(absolute_path)
    directory_name = _directory_for_absolute_path(absolute_path)

    local_file_storage = LocalFileSystemBucket(directory_name)
    return local_file_storage.download_as_string(file_name)

def _directory_for_absolute_path(absolute_path):
    import os.path as path
    return path.dirname(absolute_path)

def _file_name_from_absolute_path(absolute_path):
    import os.path as path
    return path.basename(absolute_path)