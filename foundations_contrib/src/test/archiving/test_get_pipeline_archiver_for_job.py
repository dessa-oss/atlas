"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from foundations_contrib.archiving import get_pipeline_archiver_for_job

class TestGetPipelineArchiverForJob(Spec):

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

    def test_get_pipeline_archive_for_job_returns_correct_pipeline_archiver_for_job_id(self):
        self.assertEqual(self.pipeline_archiver, get_pipeline_archiver_for_job(self.job_id))