"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_spec.helpers import let, set_up, set_up_class, tear_down, tear_down_class 
from foundations_spec.helpers.mock_mixin import MockMixin
from foundations_spec.helpers.let_mixin import LetMixin
from foundations_spec.helpers.let_now_mixin import LetNowMixin
from contextlib import contextmanager

class Spec(unittest.TestCase, MockMixin, LetMixin, LetNowMixin):

    @let
    def faker(self):
        from faker import Faker
        return Faker()

    @classmethod
    def setUpClass(klass):
        klass._collect_let_nows()
        klass._collect_lets()
        for setup_class_method in klass._setup_class_methods():
            setup_class_method.evaluate(klass)

    @classmethod
    def tearDownClass(klass):
        for tear_down_class_method in klass._tear_down_class_methods():
            tear_down_class_method.evaluate(klass)
        klass._restore_original_lets()
    
    def setUp(self):
        self.__class__._collect_let_nows()
        self.__class__._collect_lets()
        self._setup_let_nows()
        for setup_method in self._setup_methods():
            setup_method.evaluate(self)

    def _setup_methods(self):
        for _, _, function in LetMixin._klass_attributes(self.__class__):
            if isinstance(function, set_up):
                yield function
    
    @classmethod
    def _setup_class_methods(klass):
        for _, _, function in LetMixin._klass_attributes(klass):
            if isinstance(function, set_up_class):
                yield function
    
    def tearDown(self):
        for tear_down_method in self._tear_down_methods():
            tear_down_method.evaluate(self)
        self._mock_tear_down()
        self._clear_lets()

    def assert_list_contains_items(self, expected, result):
        for item in expected:
            if not item in result:
                raise AssertionError('Expected to find {} in {}'.format(item, result))

    @contextmanager
    def assert_does_not_raise(self):
        try:
            yield
        except Exception as error:
            error_class = error.__class__.__name__
            raise AssertionError("Expected not to raise error, but got {} with '{}'".format(error_class, error))

    def _tear_down_methods(self):
        for _, _, function in LetMixin._klass_attributes(self.__class__):
            if isinstance(function, tear_down):
                yield function

    @classmethod
    def _tear_down_class_methods(klass):
        for _, _, function in LetMixin._klass_attributes(klass):
            if isinstance(function, tear_down_class):
                yield function
