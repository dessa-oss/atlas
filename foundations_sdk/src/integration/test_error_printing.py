"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

import foundations
import integration.fixtures.stages as stages

class TestErrorPrinting(unittest.TestCase):
    def setUp(self):
        import sys
        sys.excepthook = sys.__excepthook__

    def test_restores_excepthook_on_successful_stage(self):
        import sys

        make_data = foundations.create_stage(stages.make_data)
        data = make_data("data")
        data.run_same_process()

        self.assertEqual(sys.excepthook, sys.__excepthook__)

    def test_restores_excepthook_upon_error_catch(self):
        import sys

        divide_by_zero = foundations.create_stage(stages.divide_by_zero)
        data = divide_by_zero()
        
        try:
            data.run_same_process()
            self.fail("Bad test - this should have thrown an exception.")
        except:
            self.assertEqual(sys.excepthook, sys.__excepthook__)