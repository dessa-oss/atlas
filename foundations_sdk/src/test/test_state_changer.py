"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_contrib.state_changer import StateChanger
import foundations_internal


class TestStateChanger(unittest.TestCase):

    class MockClass(object):
        pass

    class MockPipeline(object):
        pass

    class MockPipelineContext(object):
        pass

    def test_changes_state(self):
        pipeline = self.MockPipeline()
        with StateChanger('foundations_internal', 'pipeline', pipeline):
            self.assertEqual(
                pipeline, foundations_internal.pipeline)

    def test_changes_state_different_context(self):
        pipeline_context = self.MockPipelineContext()
        with StateChanger('foundations_internal', 'pipeline_context', pipeline_context):
            self.assertEqual(
                pipeline_context, foundations_internal.pipeline_context)

    def test_changes_state_namespaced_value(self):
        import foundations_internal.argument

        foundations_internal.argument.MockClass = self.MockClass()

        mock_class = self.MockClass()
        with StateChanger('foundations_internal.argument', 'MockClass', mock_class):
            self.assertEqual(
                mock_class, foundations_internal.argument.MockClass)

    def test_resets_state(self):
        previous_pipeline = foundations_internal.pipeline
        pipeline = self.MockPipelineContext()
        with StateChanger('foundations_internal', 'pipeline', pipeline):
            pass
        self.assertEqual(
            previous_pipeline, foundations_internal.pipeline)

    def test_resets_state_different_context(self):
        previous_context = foundations_internal.pipeline_context
        pipeline_context = self.MockPipelineContext()
        with StateChanger('foundations_internal', 'pipeline_context', pipeline_context):
            pass
        self.assertEqual(
            previous_context, foundations_internal.pipeline_context)
