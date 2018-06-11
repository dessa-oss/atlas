"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class NullArchive(object):

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def append(self, name, item, prefix=None):
        pass

    def append_binary(self, name, serialized_item, prefix=None):
        pass

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        pass

    def fetch(self, name, prefix=None):
        return None

    def fetch_binary(self, name, prefix=None):
        return None

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        pass
