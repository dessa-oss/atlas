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
            for function_name, function in klass.__dict__.items():
                if isinstance(function, let):
                    functions_to_remove.append(function_name)
                    klass._lets[function_name] = function
            
            for function_name in functions_to_remove:
                delattr(klass, function_name)
