"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ConstantParameter(object):

    def __init__(self, value):
        self._value = value

    def compute_value(self, runtime_data):
        return self._value

    def provenance(self):
        return {'type': 'constant', 'value': self._value}

    def hash(self, runtime_data):
        from foundations.utils import generate_uuid
        return generate_uuid(str(self._value))

    def enable_caching(self):
        pass

    def __str__(self):
        return self._value.__str__()
