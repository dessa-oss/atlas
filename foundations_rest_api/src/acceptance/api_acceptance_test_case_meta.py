"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class APIAcceptanceTestCaseMeta(type):

    def __new__(metaclass, name, bases, attributes):
        if name == 'APIAcceptanceTestCaseBase':
            return metaclass._construct_parent_class(name, bases, attributes)
        else:
            return metaclass._construct_child_class(name, bases, attributes)

    @classmethod
    def _construct_parent_class(metaclass, name, bases, attributes):
        return type.__new__(metaclass, name, bases, attributes)

    @classmethod
    def _construct_child_class(metaclass, name, bases, attributes):
        custom_base_class = metaclass._get_custom_base_class(bases, attributes)
        klass = metaclass._get_child_class(name, custom_base_class, attributes)
        klass._check_mandatory_attributes()
        test_methods_names = custom_base_class._setup_test_methods()
        klass._force_child_class_implementation(test_methods_names)
        return klass

    @classmethod
    def _get_custom_base_class(metaclass, bases, attributes):
        return type.__new__(metaclass, metaclass._get_base_class_name(), bases, attributes)

    @classmethod
    def _get_child_class(metaclass, name, custom_base_class, attributes):
        return type.__new__(metaclass, name, (custom_base_class,), attributes)

    @classmethod
    def _get_base_class_name(metaclass):
        from uuid import uuid4
        uuid = str(uuid4()).replace('-', '')
        return ''.join(['APIAcceptanceTestCaseCustomBase', uuid])

    def _check_mandatory_attributes(klass):
        if (not getattr(klass, 'url', None) or
            getattr(klass, 'sorting_columns', None) is None or
            getattr(klass, 'filtering_columns', None) is None):
            raise NotImplementedError('You must define class attributes "url", "sorting_columns" and "filtering_columns"')

    def _force_child_class_implementation(klass, test_method_names):
        not_implemented = [method_name for method_name in test_method_names if method_name not in klass.__dict__]
        if not_implemented:
            not_implemented = ', '.join(not_implemented)
            message = 'The following methods must be added to {}: {}'.format(klass.__name__, not_implemented)
            raise NotImplementedError(message)
