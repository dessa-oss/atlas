"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_contrib.helpers.argument_namer import ArgumentNamer


class TestArgumentNamer(unittest.TestCase):

    def test_function_no_arguments(self):
        def function_no_arguments():
            pass

        namer = ArgumentNamer(function_no_arguments, (), {})
        self.assertEqual([], namer.name_arguments())

    def test_function_single_named_arguments(self):
        def function_one_argument(a):
            pass

        namer = ArgumentNamer(function_one_argument, (), {'a': 2})
        self.assertEqual([('a', 2)], namer.name_arguments())

    def test_function_multiple_named_arguments(self):
        def function_three_arguments(a, b, c):
            pass

        namer = ArgumentNamer(function_three_arguments,
                              (), {'c': 5, 'a': 2, 'b': 4})
        self.assertEqual([('a', 2), ('b', 4), ('c', 5)],
                         namer.name_arguments())

    def test_function_single_unnamed_argument(self):
        def function_single_unnamed_arg(a):
            pass

        namer = ArgumentNamer(function_single_unnamed_arg, (9,), {})
        self.assertEqual([('a', 9)], namer.name_arguments())

    def test_function_multiple_unnamed_argument(self):
        def function_multiple_unnamed_arg(a, b):
            pass

        namer = ArgumentNamer(function_multiple_unnamed_arg, (9, 20), {})
        self.assertEqual([('a', 9), ('b', 20)], namer.name_arguments())

    def test_function_one_unnamed_one_named_argument(self):
        def function_one_named_one_unnamed_argument(a, b):
            pass

        namer = ArgumentNamer(
            function_one_named_one_unnamed_argument, (8,), {'b': 21})
        self.assertEqual([('a', 8), ('b', 21)], namer.name_arguments())

    def test_function_one_named_one_unnamed_argument(self):
        def function_one_unnamed_one_named_argument(a, b):
            pass

        namer = ArgumentNamer(
            function_one_unnamed_one_named_argument, (8,), {'a': 21})
        self.assertEqual([('a', 21), ('b', 8)], namer.name_arguments())

    def test_function_var_args(self):
        def function_with_args(*args):
            pass

        namer = ArgumentNamer(function_with_args, (1, 2), {})
        self.assertEqual([('<args>', 1), ('<args>', 2)],
                         namer.name_arguments())

    def test_function_different_var_args(self):
        def function_with_args(*args):
            pass

        namer = ArgumentNamer(function_with_args, (31, 4), {})
        self.assertEqual([('<args>', 31), ('<args>', 4)],
                         namer.name_arguments())

    def test_function_unnamed_and_var_args(self):
        def function_with_args_and_unnamed_args(a, *args):
            pass

        namer = ArgumentNamer(function_with_args_and_unnamed_args, (31, 4), {})
        self.assertEqual([('a', 31), ('<args>', 4)], namer.name_arguments())

    def test_function_with_var_kwargs(self):
        def function_with_kwags(**kwargs):
            pass

        namer = ArgumentNamer(function_with_kwags, (), {'a': 10, 'b': 9})
        self._assert_list_contains_items([('a', 10), ('b', 9)], namer.name_arguments())

    def test_function_with_different_var_kwargs(self):
        def function_with_kwags(**kwargs):
            pass

        namer = ArgumentNamer(function_with_kwags, (), {'a': 89, 'b': 1})
        self._assert_list_contains_items([('a', 89), ('b', 1)], namer.name_arguments())

    def test_function_with_kwargs_and_unnamed_arguments(self):
        def function_with_kwargs_and_unnamed_arguments(a, **kwargs):
            pass

        namer = ArgumentNamer(
            function_with_kwargs_and_unnamed_arguments, (89,), {'b': 1})
        self._assert_list_contains_items([('a', 89), ('b', 1)], namer.name_arguments())

    def test_function_with_default_values(self):
        def function_with_default_values(a=5):
            pass

        namer = ArgumentNamer(function_with_default_values, (), {})
        self.assertEqual([('a', 5)], namer.name_arguments())

    def test_function_with_different_default_values(self):
        def function_with_different_default_values(b=35, c=66):
            pass

        namer = ArgumentNamer(function_with_different_default_values, (), {})
        self.assertEqual([('b', 35), ('c', 66)], namer.name_arguments())

    def test_function_with_one_default_value(self):
        def function_with_one_default_value(b, c=566):
            pass

        namer = ArgumentNamer(function_with_one_default_value, (135,), {})
        self.assertEqual([('b', 135), ('c', 566)], namer.name_arguments())

    def test_function_with_instance(self):
        namer = ArgumentNamer(self._function_with_instance, (), {})
        self.assertEqual([('self', self)], namer.name_arguments())

    def test_function_with_instance_and_args(self):
        namer = ArgumentNamer(self._function_with_instance_and_args, (5,), {})
        self.assertEqual([('self', self), ('a', 5)], namer.name_arguments())

    def _function_with_instance(self):
        pass

    def _function_with_instance_and_args(self, a):
        pass

    def _assert_list_contains_items(self, expected, result):
        has_items = True
        for item in expected:
            has_items = has_items and item in result
        self.assertTrue(has_items)
