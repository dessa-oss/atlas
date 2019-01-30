"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class LetMixin(object):
    
    def __getattr__(self, name):
        if name == '_lets':
            return None

        lets = self.__class__._lets
        if name in lets:
            value = lets[name](self)
            setattr(self, name, value)
            return value

        raise AttributeError(self._missing_attribute_message(name))

    def _missing_attribute_message(self, name):
        return "'{}' object has no attribute '{}'".format(self.__class__.__name__, name)

    @classmethod
    def _collect_lets(klass):
        from foundations_internal.testing.helpers import let

        if getattr(klass, '_lets', None) is None:
            klass._lets = {}

        functions_to_remove = []
        for function_name, klass_having_function, function in LetMixin._klass_attributes(klass):
            if isinstance(function, let):
                functions_to_remove.append((klass_having_function, function_name))
                klass._lets[function_name] = function
        
        for klass_having_function, function_name in functions_to_remove:
            delattr(klass_having_function, function_name)

    @staticmethod
    def _klass_attributes(klass):
        for name in dir(klass):
            klass_having_attribute, attribute = LetMixin._get_klass_attribute(klass, name)
            yield name, klass_having_attribute, attribute
    
    @staticmethod
    def _get_klass_attribute(klass, name):
        if name in klass.__dict__:
            return klass, getattr(klass, name)

        for base_klass in klass.__bases__:
            klass_having_attribute, attribute = LetMixin._get_klass_attribute(base_klass, name)
            if klass_having_attribute:
                return klass_having_attribute, attribute
        
        return None, None