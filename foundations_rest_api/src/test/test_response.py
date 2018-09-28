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

    class MockModelTwo(PropertyModel):
        some_data = PropertyModel.define_property()
        some_other_data = PropertyModel.define_property()

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

    def test_as_json(self):
        mock = self.Mock(self.MockModel(data='hello'))
        response = Response('mock', mock.value)
        self.assertEqual({'data': 'hello'}, response.as_json())

    def test_as_json_filter_properties(self):
        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data='world'))
        response = Response('mock', mock.value)
        self.assertEqual({'some_data': 'hello'}, response.only(['some_data']).as_json())

    def test_as_json_filter_properties_different_property(self):
        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data='world'))
        response = Response('mock', mock.value)
        self.assertEqual({'some_other_data': 'world'}, response.only(['some_other_data']).as_json())

    def test_as_json_filter_properties_in_list(self):
        mock = self.Mock([self.MockModelTwo(some_data='hello', some_other_data='world')])
        response = Response('mock', mock.value)
        self.assertEqual([{'some_data': 'hello'}], response.only(['some_data']).as_json())

    def test_as_json_filter_properties_in_list_of_response(self):
        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data='world'))
        response = Response('mock', mock.value)

        mock_two = self.Mock([response])
        response = Response('mock', mock_two.value)
        self.assertEqual([{'some_data': 'hello'}], response.only(['some_data']).as_json())

    def test_as_json_filter_properties_multiple_properties(self):
        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data='world'))
        response = Response('mock', mock.value)
        self.assertEqual({'some_data': 'hello', 'some_other_data': 'world'}, response.only(['some_data', 'some_other_data']).as_json())

    def test_as_json_different_action(self):
        mock = self.Mock(self.MockModel(data='hello world'))
        response = Response('mock', mock.value)
        self.assertEqual({'data': 'hello world'}, response.as_json())

    def test_as_json_recursive_response(self):
        mock = self.Mock('hello world')
        response = Response('mock', mock.value)

        mock2 = self.Mock(self.MockModel(data=response))
        response2 = Response('mock', mock2.value)

        self.assertEqual({'data': 'hello world'}, response2.as_json())

    def test_as_json_recursive_response_via_dictionary(self):
        mock = self.Mock('hello world')
        response = Response('mock', mock.value)

        mock2 = self.Mock({'data': response})
        response2 = Response('mock', mock2.value)

        self.assertEqual({'data': 'hello world'}, response2.as_json())

    def test_as_json_recursive_response_via_list(self):
        mock = self.Mock('hello world')
        response = Response('mock', mock.value)

        mock2 = self.Mock([response])
        response2 = Response('mock', mock2.value)

        self.assertEqual(['hello world'], response2.as_json())

    def test_as_json_recursive_response_via_response_in_property_containing_model(self):
        mock = self.Mock([self.MockModel(data='hello world')])
        response = Response('mock', mock.value)

        mock2 = self.Mock(self.MockModel(data=response))
        response2 = Response('mock', mock2.value)

        self.assertEqual({'data': [{'data': 'hello world'}]}, response2.as_json())

    def test_as_json_non_property(self):
        mock = self.Mock('hello world')
        response = Response('mock', mock.value)
        self.assertEqual('hello world', response.as_json())

    def test_as_json_list(self):
        mock = self.Mock(['hello', 'world'])
        response = Response('mock', mock.value)
        self.assertEqual(['hello', 'world'], response.as_json())

    def test_as_json_with_parent(self):
        mock_parent = self.Mock('hello world')
        response_parent = Response('mock', mock_parent.value)
        
        mock = self.Mock('hello world')
        response = Response('mock', mock.value, response_parent)

        response.evaluate()
        self.assertTrue(mock_parent.called)
