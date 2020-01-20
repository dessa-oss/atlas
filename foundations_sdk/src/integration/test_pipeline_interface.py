"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import unittest


class TestPipelineInterface(unittest.TestCase):
    def test_simple_callback(self):
        import staged_integration.fixtures.stages as staged_stages
        import integration.fixtures.stages as stages

        self.assertEqual(staged_stages.make_data().run_same_process(), stages.make_data())
