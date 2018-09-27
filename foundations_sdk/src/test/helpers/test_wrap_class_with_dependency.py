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

        def load(self, dependency):
            self.dependency = dependency

        def another_load(self, another_dependency):
            self.another_dependency = another_dependency

        def fn_that_returns(self, dependency):
            return dependency*2

        def load_with_params(self, dependency, arg, kwarg):
            self.arg = arg
            self.kwarg = kwarg

    @wrap_class_with_dependency(MockWrappedClass, 'load', 'another_load', 'fn_that_returns', 'load_with_params')
    class MockClassWrapper(object):

        def wrapped(self):
            return self._wrapped

    @wrap_class_with_dependency(MockWrappedClass, 'load')
    class MockClassWrapper_2(object):
        pass

    def test_stores_wrapped_class(self):
        mock = self.MockClassWrapper(None)
        self.assertTrue(isinstance(mock.wrapped(), self.MockWrappedClass))

    def test_calls_wrapped_class_method(self):
        mock = self.MockClassWrapper(None)
        mock.arb_method()
        self.assertTrue(mock.wrapped().flag)

    def test_calls_wrapped_class_different_method(self):
        mock = self.MockClassWrapper(None)
        mock.another_arb_method()
        self.assertTrue(mock.wrapped().another_flag)

    def test_calls_invalid_method(self):
        mock = self.MockClassWrapper(None)
        with self.assertRaises(AttributeError) as context:
            mock.bad_method()

        self.assertIn(
            "'MockClassWrapper' object has no attribute 'bad_method'", context.exception.args)

    def test_calls_invalid_method_different_class_different_method(self):
        mock = self.MockClassWrapper_2(None)
        with self.assertRaises(AttributeError) as context:
            mock.different_bad_method()

        self.assertIn(
            "'MockClassWrapper_2' object has no attribute 'different_bad_method'", context.exception.args)

    def test_load_dependency(self):
        dependency = object()
        mock = self.MockClassWrapper(dependency)
        mock.load()
        self.assertEquals(dependency, mock.wrapped().dependency)

    def test_load_dependency_with_different_method(self):
        another_dependency = object()
        mock = self.MockClassWrapper(another_dependency)
        mock.another_load()
        self.assertEquals(another_dependency,
                          mock.wrapped().another_dependency)

    def test_load_dependency_invalid_dependency(self):
        dependency = object()
        mock = self.MockClassWrapper_2(dependency)
        with self.assertRaises(TypeError) as context:
            mock.another_load()

        self.assertIn(
            "another_load() missing 1 required positional argument: 'another_dependency'", context.exception.args)

    def test_load_dependency_with_return_value(self):
        dependency = 4
        mock = self.MockClassWrapper(dependency)
        self.assertEquals(8, mock.fn_that_returns())

    def test_load_dependency_with_different_return_value(self):
        dependency = 6
        mock = self.MockClassWrapper(dependency)
        self.assertEquals(12, mock.fn_that_returns())

    def test_load_with_arguments(self):
        another_dependency = object()
        mock = self.MockClassWrapper(another_dependency)
        mock.load_with_params('hello', kwarg=4)
        self.assertEquals('hello', mock.wrapped().arg)
        self.assertEquals(4, mock.wrapped().kwarg)
