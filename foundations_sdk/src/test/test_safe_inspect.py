"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""

import unittest
from mock import patch

import foundations.safe_inspect as inspect

def fake_uuid4(to_return):
    def _uuid4():
        return to_return

    return _uuid4

class TestSafeInspect(unittest.TestCase):
    def test_try_get_source_code_in_memory(self):
        my_function_string = "self._my_function = lambda x: x"
        exec(my_function_string)

        uuid = "this_uuid"

        with patch('uuid.uuid4', fake_uuid4(uuid)):
            self.assertEqual(inspect.getsource(self._my_function), "<could not get source code ({})>".format(uuid))

    def test_try_get_source_code_builtin(self):
        uuid = "that_uuid"

        with patch('uuid.uuid4', fake_uuid4(uuid)):
            self.assertEqual(inspect.getsource(len), "<could not get source code ({})>".format(uuid))