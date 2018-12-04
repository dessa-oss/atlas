"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

import sys
from foundations.middleware.exception_hook_middleware import ExceptionHookMiddleware


class TestExceptionHookMiddleware(unittest.TestCase):
    def setUp(self):
        self._exception_hook_middleware = ExceptionHookMiddleware()
        sys.excepthook = sys.__excepthook__

    def test_good_callback_preserves_excepthook(self):
        def good_boi(args, kwargs):
            return args[0] + kwargs["asdf"]

        args = [43]
        kwargs = {"asdf": 57}
        result = self._exception_hook_middleware.call(
            None, None, None, args, kwargs, good_boi)
        self.assertEqual(result, 100)
        self.assertEqual(sys.excepthook, sys.__excepthook__)

    def test_bad_callback_changes_excepthook(self):
        def bad_boi(args, kwargs):
            return args[0] / kwargs["no"]

        args = [1]
        kwargs = {"no": 0}

        try:
            self._exception_hook_middleware.call(
                None, None, None, args, kwargs, bad_boi)
            self.fail("Bad test - should have thrown an exception")
        except:
            self.assertNotEqual(sys.excepthook, sys.__excepthook__)
