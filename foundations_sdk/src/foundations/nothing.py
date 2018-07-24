"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Nothing(object):

    def map(self, function):
        return Nothing()

    def is_present(self):
        return False

    def get(self):
        raise ValueError('Tried #get on Nothing')

    def get_or_else(self, value):
        return value

    def fallback(self, callback):
        from foundations.option import Option
        return Option(callback())

    def __eq__(self, other):
        return isinstance(other, Nothing)