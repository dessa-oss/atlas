"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from foundations_contrib.archiving import get_pipeline_archiver

class TestLoadPipelineArchiver(Spec):

    @let_now
    def foundations_context(self):
        from foundations_internal.foundations_context import FoundationsContext
        return self.patch('foundations_contrib.global_state.foundations_context', FoundationsContext(self.pipeline))

    @let_now
    def pipeline_context(self):
        from foundations_internal.pipeline_context import PipelineContext
        return PipelineContext()

    @let_now
    def pipeline(self):
        from foundations_internal.pipeline import Pipeline
        return Pipeline(self.pipeline_context)

    @set_up
    def set_up_foundations_context(self):
        self.pipeline_context.file_name = self.job_id

    @let
    def job_id(self):
        return self.faker.sha1()

    @let_now
    def artifact_archive(self):
        archive = Mock()
        load_archive = self.patch('foundations_contrib.archiving.load_archive', ConditionalReturn())
        load_archive.return_when(archive, 'artifact_archive')
        return archive

    @let_now
    def pipeline_archiver(self):
        instance = Mock()
        klass = self.patch('foundations_internal.pipeline_archiver.PipelineArchiver', ConditionalReturn())
        klass.return_when(instance, self.job_id, None, None, None, None, None, self.artifact_archive, None)
        return instance

    def test_pipeline_archiver_returns_a_pipeline_archiver_for_given_job_id(self):
        self.assertEqual(self.pipeline_archiver, get_pipeline_archiver())