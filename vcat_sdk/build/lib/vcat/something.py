"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Something(object):

    def __init__(self, value):
        self._value = value

    def map(self, function):
        return Something(function(self._value))

    def is_present(self):
        return True

    def get(self):
        return self._value

    def get_or_else(self, value):
        return self.get()

    def fallback(self, callback):
        return self

    def __eq__(self, other):
        if isinstance(other, Something):
            return self._value == other._value
        else:
            return False