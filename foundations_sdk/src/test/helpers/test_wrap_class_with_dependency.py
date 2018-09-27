"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.helpers.wrap_class_with_dependency import wrap_class_with_dependency


class TestWrapClassWithDependency(unittest.TestCase):

    class MockWrappedClass(object):

        def arb_method(self):
            self.flag = True

        def another_arb_method(self):
            self.another_flag = True
        
    @wrap_class_with_dependency(MockWrappedClass)
    class MockClassWrapper(object):

        def wrapped(self):
            return self._wrapped

    @wrap_class_with_dependency(MockWrappedClass)
    class MockClassWrapper_2(object):
        pass

    def test_stores_wrapped_class(self):
        mock = self.MockClassWrapper()
        self.assertTrue(isinstance(mock.wrapped(), self.MockWrappedClass))

    def test_calls_wrapped_class_method(self):
        mock = self.MockClassWrapper()
        mock.arb_method()
        self.assertTrue(mock.wrapped().flag)

    def test_calls_wrapped_class_different_method(self):
        mock = self.MockClassWrapper()
        mock.another_arb_method()
        self.assertTrue(mock.wrapped().another_flag)
    
    def test_calls_invalid_method(self):
        mock = self.MockClassWrapper()
        with self.assertRaises(AttributeError) as context:
            mock.bad_method()
            
        self.assertIn("'MockClassWrapper' object has no attribute 'bad_method'", context.exception.args)
    
    def test_calls_invalid_method_different_class_different_method(self):
        mock = self.MockClassWrapper_2()
        with self.assertRaises(AttributeError) as context:
            mock.different_bad_method()
            
        self.assertIn("'MockClassWrapper_2' object has no attribute 'different_bad_method'", context.exception.args)