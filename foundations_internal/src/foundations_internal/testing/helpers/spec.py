"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_internal.testing.helpers import let, set_up, tear_down
from foundations_internal.testing.helpers.mock_mixin import MockMixin
from foundations_internal.testing.helpers.let_mixin import LetMixin
from foundations_internal.testing.helpers.let_now_mixin import LetNowMixin

class Spec(unittest.TestCase, MockMixin, LetMixin, LetNowMixin):

    @let
    def faker(self):
        from faker import Faker
        return Faker()

    @classmethod
    def setUpClass(klass):
        klass._collect_let_nows()
        klass._collect_lets()

    @classmethod
    def tearDownClass(klass):
        klass._restore_original_lets()
    
    def setUp(self):
        self.__class__._collect_let_nows()
        self.__class__._collect_lets()
        self._setup_let_nows()
        for setup_method in self._setup_methods():
            setup_method(self)

    def _setup_methods(self):
        for function in self.__class__.__dict__.values():
            if isinstance(function, set_up):
                yield function
    
    def tearDown(self):
        for tear_down_method in self._tear_down_methods():
            tear_down_method(self)
        self._mock_tear_down()
        self._clear_lets()

    def assert_list_contains_items(self, expected, result):
        for item in expected:
            if not item in result:
                raise AssertionError('Expected to find {} in {}'.format(item, result))

    def _tear_down_methods(self):
        for function in self.__class__.__dict__.values():
            if isinstance(function, tear_down):
                yield function
