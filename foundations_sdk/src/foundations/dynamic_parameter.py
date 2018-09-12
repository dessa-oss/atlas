"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DynamicParameter(object):

    def __init__(self, hyper_parameter):
        self._hyper_parameter = hyper_parameter

    def compute_value(self, runtime_data):
        if not self._hyper_parameter.name in runtime_data:
            raise ValueError('No value provided for dynamic parameter `{}`'.format(self._hyper_parameter.name))

        return runtime_data[self._hyper_parameter.name]

    def provenance(self):
        return ('dynamic', self._hyper_parameter.name)

    def hash(self, runtime_data):
        from foundations.utils import generate_uuid

        value = self.compute_value(runtime_data)
        return generate_uuid(str(value))

    def enable_caching(self):
        pass

    def __str__(self):
        return 'parameter::{}'.format(self._hyper_parameter.name)