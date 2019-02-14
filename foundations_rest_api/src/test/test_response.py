"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock
from foundations_rest_api.response import Response
from foundations_rest_api.v1.models.property_model import PropertyModel

from foundations_internal.testing.helpers import let
from foundations_internal.testing.helpers.spec import Spec

class TestResponse(Spec):

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

    @let
    def faker(self):
        import faker
        return faker.Faker()

    @let
    def resource_name(self):
        return self.faker.name()

    @let
    def dummy_value(self):
        return self.faker.color_name()
    
    def test_resource_name_matches_input(self):
        result = Mock()
        response = Response(self.resource_name, result)
        self.assertEqual(self.resource_name, response.resource_name())

    def test_constant_returns_constant_resource(self):
        response = Response.constant(self.dummy_value)
        self.assertEqual(self.dummy_value, response.as_json())

    def test_constant_returns_constant_resource_with_status_provided(self):
        response = Response.constant(self.dummy_value, status=732)
        self.assertEqual(732, response.status())

    def test_constant_returns_constant_resource_with_default_status(self):
        response = Response.constant(self.dummy_value)
        self.assertEqual(200, response.status())
    
    def test_constant_returns_constant_resource_with_constant_name(self):
        response = Response.constant(self.dummy_value)
        self.assertEqual('Constant', response.resource_name())

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
        response = Response('mock', mock, parent=response_parent)

        response.evaluate()
        self.assertTrue(mock_parent.called)

    def test_as_json_with_fallback(self):
        mock_fallback = self.MockLazyResult('hello world')
        response_fallback = Response('mock', mock_fallback)

        mock = self.MockLazyResult(None)
        response = Response('mock', mock, fallback=response_fallback)

        response.evaluate()
        self.assertEqual('hello world', response.as_json())

    def test_as_json_with_fallback_different_fallback(self):
        mock_fallback = self.MockLazyResult('hello and goodbye to the world')
        response_fallback = Response('mock', mock_fallback)

        mock = self.MockLazyResult(None)
        response = Response('mock', mock, fallback=response_fallback)

        response.evaluate()
        self.assertEqual('hello and goodbye to the world', response.as_json())

    def test_as_json_with_no_result_and_no_fallback(self):
        mock = self.MockLazyResult(None)
        response = Response('mock', mock)

        with self.assertRaises(ValueError) as error_context:
            response.as_json()
        self.assertTrue('No response data and no fallback provided!' in error_context.exception.args)

    def test_status(self):
        mock = self.MockLazyResult('hello world')
        response = Response('mock', mock)

        self.assertEqual(200, response.status())

    def test_status_set_status(self):
        mock = self.MockLazyResult('hello world')
        response = Response('mock', mock, status=202)

        self.assertEqual(202, response.status())

    def test_status_set_status_different_status(self):
        mock = self.MockLazyResult('hello world')
        response = Response('mock', mock, status=403)

        self.assertEqual(403, response.status())

    def test_status_with_fallback(self):
        mock_fallback = self.MockLazyResult('')
        response_fallback = Response('mock', mock_fallback, status=202)

        mock = self.MockLazyResult(None)
        response = Response('mock', mock, fallback=response_fallback)

        response.evaluate()
        self.assertEqual(202, response.status())

    def test_status_with_fallback_different_fallback(self):
        mock_fallback = self.MockLazyResult('')
        response_fallback = Response('mock', mock_fallback, status=404)

        mock = self.MockLazyResult(None)
        response = Response('mock', mock, fallback=response_fallback)

        response.evaluate()
        self.assertEqual(404, response.status())

    def test_status_with_no_result_and_no_fallback(self):
        mock = self.MockLazyResult(None)
        response = Response('mock', mock)

        with self.assertRaises(ValueError) as error_context:
            response.status()
        self.assertTrue('No response data and no fallback provided!' in error_context.exception.args)

    def test_as_json_with_numpy_nan(self):
        import numpy as np

        mock = self.MockLazyResult({'hello': np.nan})
        response = Response('mock', mock)
        self.assertEqual({'hello': None}, response.as_json())

    def test_as_json_with_python_nan(self):
        mock = self.MockLazyResult({'hello': float('nan')})
        response = Response('mock', mock)
        self.assertEqual({'hello': None}, response.as_json())

    def test_as_json_nested_nan(self):
        mock = self.MockLazyResult([self.MockModel(data=float('nan'))])

        mock2 = self.MockLazyResult(self.MockModel(data=mock))
        response2 = Response('mock', mock2)

        self.assertEqual({'data': [{'data': None}]}, response2.as_json())

    def test_supports_cookie(self):
        mock = self.MockLazyResult('hello world')
        response = Response('mock', mock, cookie='Chocolate Chip')

        self.assertEqual('Chocolate Chip', response.cookie()) 

    def test_supports_cookie_different_cookie(self):
        mock = self.MockLazyResult('hello world')
        response = Response('mock', mock, cookie='Lemon Drop')

        self.assertEqual('Lemon Drop', response.cookie())
