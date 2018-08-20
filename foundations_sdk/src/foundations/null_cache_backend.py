"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class NullCacheBackend(object):

    def get(self, key):
        return None

    def get_metadata(self, key):
        return None

    def set(self, key, serialized_value, metadata, **flags):
        pass
