"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Wrapping(object):
    def __init__(self, klass, wrapped_klass, dependency_functions):
        self._klass = klass
        self._wrapped_klass = wrapped_klass
        self._dependency_functions = dependency_functions

    def wrap(self):
        for dependency_method in self._dependency_functions:
            def _inner(method_name):
                def _call_dependency_method(wrapper_instance, *args, **kwargs):
                    method = getattr(wrapper_instance._wrapped, method_name)
                    return method(wrapper_instance._dependency, *args, **kwargs)
                setattr(self._klass, method_name, _call_dependency_method)
            _inner(dependency_method)

        setattr(self._klass, '__getattr__', self._getattr())
        setattr(self._klass, '__init__', self._init())
        return self._klass

    def _getattr(self):
        def _inner(wrapper_instance, name):
            if hasattr(wrapper_instance._wrapped, name):
                return getattr(wrapper_instance._wrapped, name)
            raise AttributeError(self._missing_attribute_message(name))
        return _inner

    def _missing_attribute_message(self, name):
        return "'{}' object has no attribute '{}'".format(self._klass.__name__, name)

    def _init(self):
        def _inner(wrapper_instance, dependency):
            wrapper_instance._dependency = dependency
            wrapper_instance._wrapped = self._wrapped_klass()
        return _inner


def wrap_class_with_dependency(wrapped_klass, *dependency_functions):
    def _wrap(klass):
        return Wrapping(klass, wrapped_klass, dependency_functions).wrap()
    return _wrap
