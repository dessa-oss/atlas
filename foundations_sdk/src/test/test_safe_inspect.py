"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""

import unittest

import foundations.safe_inspect as inspect

class TestSafeInspect(unittest.TestCase):
    def test_try_get_source_code_in_memory(self):
        my_function_string = "self._my_function = lambda x: x"
        exec(my_function_string)

        self.assertEqual(inspect.getsource(self._my_function), "<could not get source code>")

    def test_try_get_source_code_builtin(self):
        self.assertEqual(inspect.getsource(len), "<could not get source code>")