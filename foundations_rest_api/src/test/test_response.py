"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.response import Response
from foundations_rest_api.v1.models.property_model import PropertyModel

class TestResponse(unittest.TestCase):

    class MockModel(PropertyModel):
        data = PropertyModel.define_property()

    class MockLazyResult(object):
        def __init__(self, value):
            self._value = value
            self.called = False

        def evaluate(self):
            self.called = True

            if isinstance(self._value, list):
                return [(item.evaluate() if isinstance(item, TestResponse.MockLazyResult) else item) for item in self._value ]

            if isinstance(self._value, TestResponse.MockLazyResult):
                return self._value.evaluate()

            if isinstance(self._value, PropertyModel):
                return self._evaluate_dict(self._value.attributes)

            if isinstance(self._value, dict):
                return self._evaluate_dict(self._value)

            return self._value

        def _evaluate_dict(self, value):
            attributes = {}
            for key, value in value.items():
                attributes[key] = value.evaluate() if isinstance(value, TestResponse.MockLazyResult) else value
            return attributes

    def test_evaluate(self):
        mock = self.MockLazyResult('hello')
        response = Response('mock', mock)
        self.assertEqual('hello', response.evaluate())

    def test_evaluate_different_action(self):
        mock = self.MockLazyResult('hello world')
        response = Response('mock', mock)
        self.assertEqual('hello world', response.evaluate())

    def test_as_json(self):
        mock = self.MockLazyResult(self.MockModel(data='hello'))
        response = Response('mock', mock)
        self.assertEqual({'data': 'hello'}, response.as_json())

    def test_as_json_different_action(self):
        mock = self.MockLazyResult(self.MockModel(data='hello world'))
        response = Response('mock', mock)
        self.assertEqual({'data': 'hello world'}, response.as_json())

    def test_as_json_recursive_response(self):
        mock = self.MockLazyResult('hello world')

        mock2 = self.MockLazyResult(self.MockModel(data=mock))
        response2 = Response('mock', mock2)

        self.assertEqual({'data': 'hello world'}, response2.as_json())

    def test_as_json_recursive_response_via_dictionary(self):
        mock = self.MockLazyResult('hello world')

        mock2 = self.MockLazyResult({'data': mock})
        response2 = Response('mock', mock2)
        self.assertEqual({'data': 'hello world'}, response2.as_json())

    def test_as_json_recursive_response_via_list(self):
        mock = self.MockLazyResult('hello world')

        mock2 = self.MockLazyResult([mock])
        response2 = Response('mock', mock2)

        self.assertEqual(['hello world'], response2.as_json())

    def test_as_json_recursive_response_via_response_in_property_containing_model(self):
        mock = self.MockLazyResult([self.MockModel(data='hello world')])

        mock2 = self.MockLazyResult(self.MockModel(data=mock))
        response2 = Response('mock', mock2)

        self.assertEqual({'data': [{'data': 'hello world'}]}, response2.as_json())

    def test_as_json_non_property(self):
        mock = self.MockLazyResult('hello world')
        response = Response('mock', mock)
        self.assertEqual('hello world', response.as_json())

    def test_as_json_list(self):
        mock = self.MockLazyResult(['hello', 'world'])
        response = Response('mock', mock)
        self.assertEqual(['hello', 'world'], response.as_json())

    def test_as_json_with_parent(self):
        mock_parent = self.MockLazyResult('hello world')
        response_parent = Response('mock', mock_parent)
        
        mock = self.MockLazyResult('hello world')
        response = Response('mock', mock, response_parent)

        response.evaluate()
        self.assertTrue(mock_parent.called)
