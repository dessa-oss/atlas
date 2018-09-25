"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

import foundations
from foundations.global_state import config_manager

class TestSmallerStackTraces(unittest.TestCase):
    def test_bad_job_default_stack_trace_is_quiet(self):
        from integration.fixtures.stages import divide_by_zero

        # default to quiet errors
        self.assertEqual(config_manager["error_verbosity"], "QUIET")

        divide_by_zero = foundations.create_stage(divide_by_zero)
        divide_by_zero_stage = divide_by_zero()

        divide_by_zero_stage.run_same_process()

    def test_bad_job_verbose_stack_trace(self):
        from integration.fixtures.stages import divide_by_zero

        config_manager["error_verbosity"] = "VERBOSE"

        divide_by_zero = foundations.create_stage(divide_by_zero)
        divide_by_zero_stage = divide_by_zero()

        try:
            divide_by_zero_stage.run_same_process()
        except:
            import sys
            import traceback

            _, _, error_trace = sys.exc_info()

            for entry in traceback.extract_tb(error_trace):
                print(entry)