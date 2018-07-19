"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StageConfig(object):

    def __init__(self):
        self._is_persisted = False
        self._cache_name = None
        self._allow_caching = False
        
    def persisted(self):
        return self._is_persisted

    def persist(self):
        self._is_persisted = True
        
    def cache_name(self):
        return self._cache_name

    def cache(self, name):
        self._cache_name = name

    def allow_caching(self):
        return self._allow_caching

    def enable_caching(self):
        self._allow_caching = True

    def disable_caching(self):
        self._allow_caching = False
