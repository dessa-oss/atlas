"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
from foundations_orbit_rest_api.lazy_result import LazyResult
from foundations_orbit_rest_api.v1.models.property_model import PropertyModel

class TestLazyResult(unittest.TestCase):

    class MockModel(PropertyModel):
        data = PropertyModel.define_property()
 
    class MockModelTwo(PropertyModel):
        some_data = PropertyModel.define_property()
        some_other_data = PropertyModel.define_property()

    class Mock(object):

        def __init__(self, value):
            self._value = value
    
        def value(self):
            self.called = True
            return self._value

    class ErrorMock(object):
        
        def value(self):
            raise Exception('Should not be called')

    def test_lazy_result(self):
        mock = self.Mock('hello world')
        lazy_result = LazyResult(mock.value)

        self.assertEqual('hello world', lazy_result.evaluate())

    def test_lazy_result_only_filter_properties(self):
        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data='world'))
        lazy_result = LazyResult(mock.value)
        self.assertEqual({'some_data': 'hello'}, lazy_result.only(['some_data']).evaluate())

    def test_lazy_result_only_does_not_filter_too_much(self):
        parent_mock = self.Mock(self.MockModel(data='hello'))
        parent_lazy_result = LazyResult(parent_mock.value)

        mock = self.Mock(self.MockModelTwo(some_data=parent_lazy_result, some_other_data='world'))
        lazy_result = LazyResult(mock.value)

        result = lazy_result.only(['some_data']).evaluate()
        self.assertEqual(['some_data'], list(result.keys()))
        self.assertEqual({'data': 'hello'}, result['some_data'].attributes)

    def test_lazy_result_only_filter_properties_different_property(self):
        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data='world'))
        lazy_result = LazyResult(mock.value)
        self.assertEqual({'some_other_data': 'world'}, lazy_result.only(['some_other_data']).evaluate())

    def test_lazy_result_only_filter_properties_in_list(self):
        mock = self.Mock([self.MockModelTwo(some_data='hello', some_other_data='world')])
        lazy_result = LazyResult(mock.value)
        self.assertEqual([{'some_data': 'hello'}], lazy_result.only(['some_data']).evaluate())

    def test_lazy_result_only_filter_properties_in_list_of_lazy_results(self):
        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data='world'))
        lazy_result = LazyResult(mock.value)

        mock_two = self.Mock([lazy_result])
        lazy_result = LazyResult(mock_two.value)
        self.assertEqual([{'some_data': 'hello'}], lazy_result.only(['some_data']).evaluate())

    def test_lazy_result_only_filter_properties_multiple_properties(self):
        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data='world'))
        lazy_result = LazyResult(mock.value)
        self.assertEqual({'some_data': 'hello', 'some_other_data': 'world'}, lazy_result.only(['some_data', 'some_other_data']).evaluate())
    
    def test_lazy_result_only_does_not_evaluate_other_properties(self):
        should_not_call_mock = self.ErrorMock()
        should_not_call_result = LazyResult(should_not_call_mock.value)

        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data=should_not_call_result))
        lazy_result = LazyResult(mock.value)

        lazy_result.only(['some_data']).evaluate()
    
    def test_lazy_result_only_does_not_evaluate_other_properties_in_list(self):
        should_not_call_mock = self.ErrorMock()
        should_not_call_result = LazyResult(should_not_call_mock.value)

        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data=should_not_call_result))
        lazy_result = LazyResult(mock.value)

        mock2 = self.Mock([lazy_result])
        lazy_result = LazyResult(mock2.value)

        lazy_result.only(['some_data']).evaluate()
    
    def test_lazy_result_only_does_not_evaluate_other_properties_recursively(self):
        should_not_call_mock = self.ErrorMock()
        should_not_call_result = LazyResult(should_not_call_mock.value)

        mock = self.Mock(self.MockModelTwo(some_data='hello', some_other_data=should_not_call_result))
        lazy_result = LazyResult(mock.value)

        mock2 = self.Mock(lazy_result)
        lazy_result = LazyResult(mock2.value)

        lazy_result.only(['some_data']).evaluate()

    def test_recursive_lazy_result(self):
        mock = self.Mock('hello world')
        lazy_result = LazyResult(mock.value)

        mock2 = self.Mock(lazy_result)
        lazy_result2 = LazyResult(mock2.value)

        self.assertEqual('hello world', lazy_result2.evaluate())

    def test_recursive_lazy_result_via_lazy_result_in_property_containing_model(self):
        mock = self.Mock([self.MockModel(data='hello world')])
        lazy_result = LazyResult(mock.value)

        mock2 = self.Mock(self.MockModel(data=lazy_result))
        lazy_result2 = LazyResult(mock2.value)

        result_attributes = lazy_result2.evaluate().attributes
        self.assertEqual(['data'], list(result_attributes.keys()))
        self.assertEqual({'data': 'hello world'}, result_attributes['data'][0].attributes)

    def test_recursive_lazy_result_via_dictionary(self):
        mock = self.Mock('hello world')
        lazy_result = LazyResult(mock.value)

        mock2 = self.Mock({'data': lazy_result})
        lazy_result2 = LazyResult(mock2.value)

        self.assertEqual({'data': 'hello world'}, lazy_result2.evaluate())

    def test_recursive_lazy_result_via_list(self):
        mock = self.Mock('hello world')
        lazy_result = LazyResult(mock.value)

        mock2 = self.Mock([lazy_result])
        lazy_result2 = LazyResult(mock2.value)

        self.assertEqual(['hello world'], lazy_result2.evaluate())
    
    def test_map_evaluates_lazy_result_and_callback(self):
        mock = self.Mock('hello world')
        lazy_result = LazyResult(mock.value)

        def _callback(result):
            return result +' result'
        
        self.assertEqual(lazy_result.map(_callback).evaluate(), 'hello world result')
