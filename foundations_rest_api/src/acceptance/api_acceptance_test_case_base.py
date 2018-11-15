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

    def __new__(metaclass, *args, **kwargs):
        klass = type.__new__(metaclass, *args, **kwargs)
        if klass.__name__ not in ('APIAcceptanceTestCaseBase', '_APIAcceptanceTestCaseMeta'):
            if not (getattr(klass, 'url', None) and getattr(klass, 'sorting_columns', None)):
                raise NotImplementedError('You must define class attributes "url" and "sorting_columns"')
            test_methods_names = APIAcceptanceTestCaseBase.setup_test_methods(klass.sorting_columns)
            klass._force_child_class_implementation(test_methods_names)
            klass.client = app_manager.app().test_client()
        return klass

    def _force_child_class_implementation(klass, test_method_names):
        not_implemented = [method_name for method_name in test_method_names if method_name not in klass.__dict__]
        if not_implemented:
            not_implemented = ', '.join(not_implemented)
            msg = 'The following methods must be added to the test case: {}'.format(not_implemented)
            raise NotImplementedError(msg)

class APIAcceptanceTestCaseBase(with_metaclass(_APIAcceptanceTestCaseMeta, unittest.TestCase)):

    @classmethod
    def setup_test_methods(klass, sorting_columns):
        klass._sorting_columns = sorting_columns
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
        for sorting_column in klass._sorting_columns:
            methods_names += add_route_sorted_methods(sorting_column)
        return methods_names

    @classmethod
    def _set_methods_for_sorted_route_all_columns(klass):

        def get_sort_param_all_columns(descending=True):

            def get_param_method():
                param_value = ','.join([('-' if descending else '') + column for column in klass._sorting_columns])
                return '?sort=' + param_value

            return get_param_method

        if len(klass._sorting_columns) > 1:
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
                return [prefix_column(*item) for item in enumerate(klass._sorting_columns)]

            def get_param_method():
                param_value = ','.join(get_prefixed_columns_list())
                return '?sort=' + param_value

            return get_param_method

        if len(klass._sorting_columns) > 1:
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
