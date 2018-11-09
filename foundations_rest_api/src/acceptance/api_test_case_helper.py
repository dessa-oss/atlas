"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
import json
from foundations_rest_api.global_state import app_manager


class APITestCaseHelperMeta(type):

    def __new__(mcls, *args, **kwargs):
        cls = super().__new__(mcls, *args, **kwargs)
        if cls.__name__ not in ('APITestCaseHelper', 'APITestCaseHelperMeta'):
            if not (getattr(cls, 'url', None) and getattr(cls, 'sorting_columns', None)):
                raise NotImplementedError('You must define class attributes "url" and "sorting_columns"')
            test_methods_names = APITestCaseHelper.setup_test_methods(cls.sorting_columns)
            cls._force_child_class_implementation(test_methods_names)
            cls.client = app_manager.app().test_client()
        return cls

    def _force_child_class_implementation(cls, test_method_names):
        not_implemented = [method_name for method_name in test_method_names if method_name not in cls.__dict__]
        if not_implemented:
            not_implemented = str(not_implemented).translate(str.maketrans({"[": "", "]": "", "'": ""}))
            msg = 'The following methods must be added to the test case: {}'.format(not_implemented)
            raise NotImplementedError(msg)


class APITestCaseHelper(unittest.TestCase, metaclass=APITestCaseHelperMeta):

    @classmethod
    def setup_test_methods(cls, sorting_columns):
        cls._sorting_columns = sorting_columns
        test_methods_1 = cls._set_abstract_method_for_normal_route()
        test_methods_2 = cls._set_abstract_methods_for_sorted_route()
        return test_methods_1 + test_methods_2

    @classmethod
    def _set_abstract_methods_for_sorted_route(cls):

        def get_test_method_sorted_route(column, parent_method_name):
            def get_sort_param_for_column(column, parent_method_name):
                sign = '-' if parent_method_name.endswith('descendant') else ''
                return '?sort={}{}'.format(sign, column)

            def test_get_route_sorted(self):
                resp = self.client.get(self.url + get_sort_param_for_column(column, parent_method_name))
                self.assertEqual(resp.status_code, 200)
                return json.loads(resp.data)

            return test_get_route_sorted

        methods_names = []
        for sorting_column in cls._sorting_columns:
            method_name_descendant = 'test_get_route_with_{}_sorted_descendant'.format(sorting_column)
            method_name_ascendant = 'test_get_route_with_{}_sorted_ascendant'.format(sorting_column)
            setattr(cls, method_name_descendant, get_test_method_sorted_route(sorting_column, method_name_descendant))
            setattr(cls, method_name_ascendant, get_test_method_sorted_route(sorting_column, method_name_ascendant))
            methods_names += [method_name_descendant, method_name_ascendant]
        return methods_names

    @classmethod
    def _set_abstract_method_for_normal_route(cls):

        def test_get_route(self):
            resp = self.client.get(self.url)
            self.assertEqual(resp.status_code, 200)
            return json.loads(resp.data)

        setattr(cls, 'test_get_route', test_get_route)
        return ['test_get_route']
