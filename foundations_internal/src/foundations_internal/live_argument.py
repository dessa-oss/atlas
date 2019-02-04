"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class LiveArgument(object):

    def __init__(self, argument, runtime_data):
        from foundations_contrib.constant_parameter import ConstantParameter
        from foundations_internal.argument import Argument

        if isinstance(argument, Argument):
            self._argument = argument
        else:
            parameter = ConstantParameter(argument)
            self._argument = Argument(None, parameter)
        self._runtime_data = runtime_data
        self._value_computed = False
        self._value = None

    def name(self):
        return self._argument.name()

    def value(self):
        if self._value_computed:
            return self._value

        self._value_computed = True

        self._value = self._argument.value(self._runtime_data)
        return self._value

    def hash(self):
        return self._argument.hash(self._runtime_data)
