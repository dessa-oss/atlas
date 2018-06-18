"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from vcat.remote_exception import *

class TestRemoteException(unittest.TestCase):
    def test_check_result_no_error(self):
        result = {"global_stage_context": {"error_information": None}}
        self.assertEqual(check_result("dummy", result, verbose_errors=True), result)

    def test_check_result_error(self):
        self.fail("fill me in!")