"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DataLoader(object):
    
    def load_data(self, file_name_with_scheme):
        import os.path as path

        from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket
        from foundations_internal.serializer import deserialize

        file_name = path.basename(file_name_with_scheme)
        directory_name = path.dirname(file_name_with_scheme)[8:]

        local_file_system_bucket = LocalFileSystemBucket(directory_name)
        serialized_data = local_file_system_bucket.download_as_string(file_name)

        return deserialize(serialized_data)