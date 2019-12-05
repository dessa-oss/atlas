"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestPipelineContextWrapper(Spec):

    def test_pipeline_context_wrapper_returns_pipeline_context(self):
        from foundations_internal.pipeline_context import PipelineContext
        from foundations_internal.pipeline_context_wrapper import PipelineContextWrapper

        pipeline_context = PipelineContext()
        pipeline_context_wrapper = PipelineContextWrapper(pipeline_context)
        self.assertEqual(pipeline_context, pipeline_context_wrapper.pipeline_context())