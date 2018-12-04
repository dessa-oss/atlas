"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class IndexAllocator(object):

    def __init__(self):
        self._count = 0
        self._mapping = {}

    def get_index(self, item):
        if item in self._mapping:
            return self._mapping[item]

        self._mapping[item] = self._count
        self._count += 1
        return self._mapping[item]
