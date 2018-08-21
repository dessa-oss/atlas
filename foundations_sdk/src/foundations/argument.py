"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Argument(object):

    @staticmethod
    def generate_from(value, name):
        from foundations.hyperparameter import Hyperparameter
        from foundations.stage_connector_wrapper import StageConnectorWrapper
        from foundations.constant_parameter import ConstantParameter
        from foundations.dynamic_parameter import DynamicParameter
        from foundations.stage_parameter import StageParameter

        if isinstance(value, Hyperparameter):
            if value.name is None:
                value.name = name
            parameter = DynamicParameter(value)
        elif isinstance(value, StageConnectorWrapper):
            parameter = StageParameter(value)
        else:
            parameter = ConstantParameter(value)

        return Argument(name, parameter)

    def __init__(self, name, parameter):
        self._name = name
        self._parameter = parameter

    def name(self):
        return self._name

    def value(self, runtime_data):
        return self._parameter.compute_value(runtime_data)

    def hash(self, runtime_data):
        return self._parameter.hash(runtime_data)

    def enable_caching(self):
        self._parameter.enable_caching()