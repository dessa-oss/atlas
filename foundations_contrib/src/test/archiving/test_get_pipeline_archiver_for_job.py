"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from foundations_contrib.archiving import get_pipeline_archiver_for_job

class TestGetPipelineArchiverForJob(Spec):

    mock_load_archive = let_patch_mock('foundations_contrib.archiving.load_archive', ConditionalReturn())
    artifact_archive = let_mock()
    job_source_archive = let_mock()
    miscellaneous_archive = let_mock()
    persisted_data_archive = let_mock()

    @let
    def job_id(self):
        return self.faker.sha1()

    @set_up
    def set_up(self):
        self.mock_load_archive.return_when(self.artifact_archive, 'artifact_archive')
        self.mock_load_archive.return_when(self.job_source_archive, 'job_source_archive')
        self.mock_load_archive.return_when(self.miscellaneous_archive, 'miscellaneous_archive')
        self.mock_load_archive.return_when(self.persisted_data_archive, 'persisted_data_archive')

    @let_now
    def pipeline_archiver(self):
        instance = Mock()
        klass = self.patch('foundations_internal.pipeline_archiver.PipelineArchiver', ConditionalReturn())
        klass.return_when(instance, self.job_id, None, None, self.persisted_data_archive, None, self.job_source_archive, self.artifact_archive, self.miscellaneous_archive)
        return instance

    def test_get_pipeline_archive_for_job_returns_correct_pipeline_archiver_for_job_id(self):
        self.assertEqual(self.pipeline_archiver, get_pipeline_archiver_for_job(self.job_id))