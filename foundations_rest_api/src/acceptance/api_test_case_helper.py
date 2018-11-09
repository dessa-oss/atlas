"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
import json
from abc import ABCMeta, abstractmethod
from foundations_rest_api.global_state import app_manager
from test.v1.models.jobs_tests_helper_mixin import JobsTestsHelperMixin


class APITestCaseHelper(unittest.TestCase, metaclass=ABCMeta):

    def setup_api_test_env(self, url, sorting_column):
        self.client = app_manager.app().test_client(self)
        self.url = url
        self.sort_query_string_asc = '?sort={}'.format(sorting_column)
        self.sort_query_string_desc = '?sort=-{}'.format(sorting_column)

    @abstractmethod
    def test_get_route(self):        
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        return json.loads(resp.data)

    @abstractmethod
    def test_get_route_sorted_descendant(self):
        resp = self.client.get(self.url + self.sort_query_string_desc)
        self.assertEqual(resp.status_code, 200)
        return json.loads(resp.data)

    @abstractmethod
    def test_get_route_sorted_ascendant(self):
        resp = self.client.get(self.url + self.sort_query_string_asc)
        self.assertEqual(resp.status_code, 200)
        return json.loads(resp.data)
