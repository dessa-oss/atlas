"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.response import Response

class TestResponse(unittest.TestCase):

    class Mock(object):
        def __init__(self, value):
            self._value = value
            self.called = False

        def value(self):
            self.called = True
            return self._value

    def test_evaluate(self):
        mock = self.Mock('hello')
        response = Response('mock', mock.value)
        self.assertEqual('hello', response.evaluate())

    def test_evaluate_different_action(self):
        mock = self.Mock('hello world')
        response = Response('mock', mock.value)
        self.assertEqual('hello world', response.evaluate())

    def test_evaluate_with_parent(self):
        mock_parent = self.Mock('hello world')
        response_parent = Response('mock', mock_parent.value)
        
        mock = self.Mock('hello world')
        response = Response('mock', mock.value, response_parent)

        response.evaluate()
        self.assertTrue(mock_parent.called)
