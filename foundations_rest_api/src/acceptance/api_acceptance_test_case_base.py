"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
import json
import itertools
from foundations_rest_api.global_state import app_manager


class _APIAcceptanceTestCaseMeta(type):

    def __new__(mcls, *args, **kwargs):
        cls = super().__new__(mcls, *args, **kwargs)
        if cls.__name__ not in ('APIAcceptanceTestCaseBase', '_APIAcceptanceTestCaseMeta'):
            if not (getattr(cls, 'url', None) and getattr(cls, 'sorting_columns', None)):
                raise NotImplementedError('You must define class attributes "url" and "sorting_columns"')
            test_methods_names = APIAcceptanceTestCaseBase.setup_test_methods(cls.sorting_columns)
            cls._force_child_class_implementation(test_methods_names)
            cls.client = app_manager.app().test_client()
        return cls

    def _force_child_class_implementation(cls, test_method_names):
        not_implemented = [method_name for method_name in test_method_names if method_name not in cls.__dict__]
        if not_implemented:
            not_implemented = ', '.join(not_implemented)
            msg = 'The following methods must be added to the test case: {}'.format(not_implemented)
            raise NotImplementedError(msg)


class APIAcceptanceTestCaseBase(unittest.TestCase, metaclass=_APIAcceptanceTestCaseMeta):

    @classmethod
    def setup_test_methods(cls, sorting_columns):
        cls._sorting_columns = sorting_columns
        return itertools.chain(
            cls._set_method_for_normal_route(),
            cls._set_methods_for_sorted_route(),
            cls._set_methods_for_sorted_route_all_columns(),
            cls._set_methods_for_sorted_route_alternation()
        )

    @classmethod
    def _get_test_route_method(cls, get_param_method=None):

        def test_method(self):
            base_url = self._get_base_url()
            params = get_param_method() if get_param_method else ''
            resp = self.client.get(base_url + params)
            self.assertEqual(resp.status_code, 200)
            return json.loads(resp.data)

        return test_method

    @classmethod
    def _set_methods_for_sorted_route(cls):

        def get_sort_param_for_column(column, descending=True):

            def get_param_method():
                sign = '-' if descending else ''
                return '?sort={}{}'.format(sign, column)

            return get_param_method

        methods_names = []
        for sorting_column in cls._sorting_columns:
            method_name_descendant = 'test_route_sorted_{}_descending'.format(sorting_column)
            method_name_ascendant = 'test_route_sorted_{}_ascending'.format(sorting_column)
            setattr(cls, method_name_descendant, cls._get_test_route_method(get_sort_param_for_column(sorting_column, descending=True)))
            setattr(cls, method_name_ascendant,  cls._get_test_route_method(get_sort_param_for_column(sorting_column, descending=False)))
            methods_names += [method_name_descendant, method_name_ascendant]
        return methods_names

    @classmethod
    def _set_methods_for_sorted_route_all_columns(cls):

        def get_sort_param_all_columns(descending=True):

            def get_param_method():
                param_value = ','.join([('-' if descending else '') + column for column in cls._sorting_columns])
                return '?sort=' + param_value

            return get_param_method

        setattr(cls, 'test_get_route_all_ascending', cls._get_test_route_method(get_sort_param_all_columns(descending=False)))
        setattr(cls, 'test_get_route_all_descending', cls._get_test_route_method(get_sort_param_all_columns(descending=True)))
        return ['test_get_route_all_ascending', 'test_get_route_all_descending'] 

    @classmethod
    def _set_methods_for_sorted_route_alternation(cls):

        def test_get_route_alternation():

            def get_param_method():
                param_value = ','.join([('' if item[0] % 2 == 0 else '-') + item[1] for item in enumerate(cls._sorting_columns)])
                return '?sort=' + param_value

            return get_param_method

        setattr(cls, 'test_get_route_alternation', cls._get_test_route_method(test_get_route_alternation()))
        return ['test_get_route_alternation']

    @classmethod
    def _set_method_for_normal_route(cls):
        setattr(cls, 'test_get_route', cls._get_test_route_method())
        return ['test_get_route']

    def _extract_url_params(self):
        params = []
        temp_param = ''
        filling_temp_param = False
        for char in self.url:
            if filling_temp_param:
                if char =='{':
                    raise Exception('Bad URL formatting')
                elif char == '}':
                    filling_temp_param = False
                    params.append(temp_param)
                    temp_param = ''
                else:
                    temp_param += char
            else:
                if char == '{':
                    filling_temp_param = True
                elif char == '}':
                    raise Exception('Bad URL formatting')
        if filling_temp_param:
            raise Exception('Bad URL formatting')
        return params

    def _get_base_url(self):
        url = self.url
        params = self._extract_url_params()
        for param in params:
            url = url.replace('{{{}}}'.format(param), getattr(self, param))
        return url
