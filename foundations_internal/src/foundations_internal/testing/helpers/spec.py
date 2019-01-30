"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_internal.testing.helpers import set_up, tear_down
from foundations_internal.testing.helpers.mock_mixin import MockMixin
from foundations_internal.testing.helpers.let_mixin import LetMixin

class Spec(unittest.TestCase, MockMixin, LetMixin):

    @classmethod
    def setUpClass(klass):
        klass._collect_lets()
    
    def setUp(self):
        self.__class__._collect_lets()
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

    def _tear_down_methods(self):
        for function in self.__class__.__dict__.values():
            if isinstance(function, tear_down):
                yield function
