"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
import json
import itertools
from six import with_metaclass
from foundations_rest_api.global_state import app_manager


class _APIAcceptanceTestCaseMeta(type):

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


class APIAcceptanceTestCaseBase(with_metaclass(_APIAcceptanceTestCaseMeta, unittest.TestCase)):
    client = app_manager.app().test_client()

    @classmethod
    def _setup_test_methods(klass):
        return itertools.chain(
            klass._set_method_for_normal_route(),
            klass._set_methods_for_sorted_route(),
            klass._set_methods_for_sorted_route_all_columns(),
            klass._set_methods_for_sorted_route_alternation()
        )

    @classmethod
    def _get_test_route_method(klass, get_param_method=None):

        def test_method(self):
            base_url = self._get_base_url()
            params = get_param_method() if get_param_method else ''
            resp = self.client.get(base_url + params)
            self.assertEqual(resp.status_code, 200)
            return json.loads(resp.data)

        return test_method

    @classmethod
    def _set_methods_for_sorted_route(klass):

        def get_sort_param_for_column(column, descending=True):

            def get_param_method():
                sign = '-' if descending else ''
                return '?sort={}{}'.format(sign, column)

            return get_param_method

        def add_route_sorted_methods(column):
            method_name_descendant = 'test_route_sorted_{}_descending'.format(sorting_column)
            method_name_ascendant = 'test_route_sorted_{}_ascending'.format(sorting_column)
            setattr(klass, method_name_descendant, klass._get_test_route_method(get_sort_param_for_column(sorting_column, descending=True)))
            setattr(klass, method_name_ascendant,  klass._get_test_route_method(get_sort_param_for_column(sorting_column, descending=False)))
            return [method_name_descendant, method_name_ascendant]

        methods_names = []
        for sorting_column in klass.sorting_columns:
            methods_names += add_route_sorted_methods(sorting_column)
        return methods_names

    @classmethod
    def _set_methods_for_sorted_route_all_columns(klass):

        def get_sort_param_all_columns(descending=True):

            def get_param_method():
                param_value = ','.join([('-' if descending else '') + column for column in klass.sorting_columns])
                return '?sort=' + param_value

            return get_param_method

        if len(klass.sorting_columns) > 1:
            setattr(klass, 'test_get_route_all_ascending', klass._get_test_route_method(get_sort_param_all_columns(descending=False)))
            setattr(klass, 'test_get_route_all_descending', klass._get_test_route_method(get_sort_param_all_columns(descending=True)))
            return ['test_get_route_all_ascending', 'test_get_route_all_descending']
        return []

    @classmethod
    def _set_methods_for_sorted_route_alternation(klass):

        def test_get_route_alternation():

            def prefix_column(index, column):
                return column if index % 2 == 0 else '-{}'.format(column)

            def get_prefixed_columns_list():
                return [prefix_column(*item) for item in enumerate(klass.sorting_columns)]

            def get_param_method():
                param_value = ','.join(get_prefixed_columns_list())
                return '?sort=' + param_value

            return get_param_method

        if len(klass.sorting_columns) > 1:
            setattr(klass, 'test_get_route_alternation', klass._get_test_route_method(test_get_route_alternation()))
            return ['test_get_route_alternation']
        return []

    @classmethod
    def _set_method_for_normal_route(klass):
        setattr(klass, 'test_get_route', klass._get_test_route_method())
        return ['test_get_route']

    def _extract_url_params(self):
        from string import Formatter
        formatter  = Formatter()
        params = [format_tuple[1] for format_tuple in formatter.parse(self.url)]
        return params

    def _get_base_url(self):
        url = self.url
        params = self._extract_url_params()
        for param in params:
            if param:
                url = url.replace('{{{}}}'.format(param), getattr(self, param))
        return url
