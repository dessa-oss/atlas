"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ContextAware(object):
    def __init__(self, function):
        self._function = function
        self.__name__ = self._function.__name__

    def function(self):
        return self._function

    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)

def context_aware(function, *args):
    if len(args) == 0:
        return ContextAware(function)
    else:
        return (ContextAware(function),) + args
