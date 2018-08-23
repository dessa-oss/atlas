"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.state_changer import StateChanger


class TestStateChanger(unittest.TestCase):

    class MockClass(object):
        pass

    class MockPipeline(object):
        pass
    
    class MockPipelineContext(object):
        pass
    
    def test_changes_state(self):
        import foundations

        pipeline = self.MockPipeline()
        with StateChanger('foundations', 'pipeline', pipeline):
            self.assertEqual(pipeline, foundations.pipeline)

    def test_changes_state_different_context(self):
        import foundations

        pipeline_context = self.MockPipelineContext()
        with StateChanger('foundations', 'pipeline_context', pipeline_context):
            self.assertEqual(pipeline_context, foundations.pipeline_context)

    def test_changes_state_namespaced_value(self):
        import foundations.argument

        foundations.argument.MockClass = self.MockClass()

        mock_class = self.MockClass()
        with StateChanger('foundations.argument', 'MockClass', mock_class):
            self.assertEqual(mock_class, foundations.argument.MockClass)

    def test_resets_state(self):
        import foundations

        previous_pipeline = foundations.pipeline
        pipeline = self.MockPipelineContext()
        with StateChanger('foundations', 'pipeline', pipeline):
            pass
        self.assertEqual(previous_pipeline, foundations.pipeline)

    def test_resets_state_different_context(self):
        import foundations

        previous_context = foundations.pipeline_context
        pipeline_context = self.MockPipelineContext()
        with StateChanger('foundations', 'pipeline_context', pipeline_context):
            pass
        self.assertEqual(previous_context, foundations.pipeline_context)
