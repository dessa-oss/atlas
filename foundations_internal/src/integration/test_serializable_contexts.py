"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_internal.pipeline_context import PipelineContext
from foundations_internal.pipeline import Pipeline


class TestSerializableContexts(unittest.TestCase):

    def setUp(self):
        self._context = PipelineContext()
        self._pipeline = Pipeline(self._context)

    def test_can_serialize_when_stage_contains_unserializable_data(self):
        from foundations_internal.serializer import serialize

        stage = self._pipeline.stage(self.input)
        stage_two = self._pipeline.stage(self.output, stage)
        stage_two.run_same_process()

        serialize(self._context)

    def test_can_serialize_when_stage_contains_unserializable_data_using_kwargs(self):
        from foundations_internal.serializer import serialize

        stage = self._pipeline.stage(self.input)
        stage_two = self._pipeline.stage(self.output, data=stage)
        stage_two.run_same_process()

        serialize(self._context)

    def input(self):
        try:
            raise Exception('ACK')
        except:
            import sys
            exception_info = sys.exc_info()
            return exception_info

    def output(self, data):
        pass
