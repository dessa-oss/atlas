"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_internal.remote_exception import *


class TestRemoteException(unittest.TestCase):
    def test_check_result_no_error(self):
        result = {"global_stage_context": {"error_information": None}}
        self.assertEqual(check_result(
            "dummy", result, verbose_errors=True), result)

    def test_check_result_error(self):
        import sys
        import traceback
        from foundations.utils import pretty_error

        try:
            1/0
        except:
            error_info = sys.exc_info()
            result = {
                "global_stage_context": {
                    "error_information": {
                        "type": error_info[0],
                        "exception": error_info[1],
                        "traceback": traceback.extract_tb(error_info[2])
                    }
                }
            }

        try:
            check_result("dummy", result, verbose_errors=True)
            self.fail("Did not throw exception")
        except RemoteException as e:
            error_information = result["global_stage_context"]["error_information"]
            self.assertEqual(str(e), pretty_error(
                "dummy", error_information, verbose=True))
        except:
            self.fail("Did not throw the proper exception")
