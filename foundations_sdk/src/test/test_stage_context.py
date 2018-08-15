"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.stage_context import StageContext


class TestStageContext(unittest.TestCase):

    def test_set_stage_output(self):
        stage_context = StageContext()
        stage_context.set_stage_output('some stage output')
        self.assertEqual('some stage output', stage_context.stage_output)

    def test_set_stage_output_has_stage_after_run(self):
        stage_context = StageContext()
        self.assertEqual(None, stage_context.has_stage_output)
        stage_context.set_stage_output('some stage output')
        self.assertTrue(stage_context.has_stage_output)

    def test_add_error_information(self):
        import sys
        stage_context = StageContext()

        mock_exception = sys.exc_info()
        stage_context.add_error_information(mock_exception)
        self.assertEqual({'type': None, 'exception': None,
                          'traceback': []}, stage_context.error_information)
