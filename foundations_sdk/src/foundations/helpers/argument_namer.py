"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ArgumentNamer(object):

    def __init__(self, function, arguments, keyword_arguments):
        self._function = function

        if hasattr(self._function, '__self__'):
            self._arguments = (self._function.__self__,) + arguments
        else:
            self._arguments = arguments
        self._keyword_arguments = keyword_arguments
    
    def name_arguments(self):
        try:
            from inspect import getfullargspec as getargspec
        except ImportError:
            from inspect import getargspec

        result = []
        argument_index = 0
        default_argument_index = 0

        argspec = getargspec(self._function)
        filled_arguments = set()


        for argument_name in argspec.args:
            if argument_name in self._keyword_arguments:
                result.append((argument_name, self._keyword_arguments[argument_name]))
            elif argument_index < len(self._arguments):
                result.append((argument_name, self._arguments[argument_index]))
                argument_index += 1
            else:
                result.append((argument_name, argspec.defaults[default_argument_index]))
                default_argument_index += 1
            filled_arguments.add(argument_name)

        while argument_index < len(self._arguments):
            result.append(('<args>', self._arguments[argument_index]))
            argument_index += 1

        for key, value in self._keyword_arguments.items():
            if key not in filled_arguments:
                result.append((key, value))

        return result
