"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

import foundations

class TestSmallerStackTraces(unittest.TestCase):
    def test_bad_job_default_stack_trace(self):
        from integration.fixtures.stages import divide_by_zero

        divide_by_zero_stage = foundations.create_stage(divide_by_zero)
        divide_by_zero_stage().run_same_process()