"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_contrib.stage_parameter import StageParameter


class TestStageParameter(unittest.TestCase):

    class MockStage(object):

        def __init__(self, name=None):
            from uuid import uuid4

            self.cache_enabled = False
            self._uuid = str(uuid4())
            self._name = name

        def enable_caching(self):
            self.cache_enabled = True

        def uuid(self):
            return self._uuid

        def function_name(self):
            return self._name

    def test_enable_caching_forwards_to_stage(self):
        stage = self.MockStage()
        parameter = StageParameter(stage)
        parameter.enable_caching()

        self.assertTrue(stage.cache_enabled)

    def test_provenance_returns_name(self):
        stage = self.MockStage('potato')
        parameter = StageParameter(stage)

        self.assertEqual({'type': 'stage', 'stage_name': 'potato',
                          'stage_uuid': stage.uuid()}, parameter.provenance())

    def test_provenance_returns_name_different_value(self):
        stage = self.MockStage('tomako')
        parameter = StageParameter(stage)

        self.assertEqual({'type': 'stage', 'stage_name': 'tomako',
                          'stage_uuid': stage.uuid()}, parameter.provenance())

    def test_str_returns_stage_and_name(self):
        stage = self.MockStage()

        parameter = StageParameter(stage)
        expected_string = 'stage::{}'.format(stage.uuid())
        self.assertEqual(expected_string, str(parameter))

    def _make_parameter(self, method, *args):
        from foundations_internal.pipeline import Pipeline
        from foundations_internal.pipeline_context import PipelineContext

        stage = Pipeline(PipelineContext()).stage(method, *args)
        return StageParameter(stage)
