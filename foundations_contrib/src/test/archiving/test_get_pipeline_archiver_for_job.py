"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from foundations_contrib.archiving import get_pipeline_archiver_for_job

class TestGetPipelineArchiverForJob(Spec):

    mock_is_job_completed = let_patch_mock('foundations_contrib.job_data_redis.JobDataRedis.is_job_completed')

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
        self.mock_is_job_completed.return_value = True
        self.assertEqual(self.pipeline_archiver, get_pipeline_archiver_for_job(self.job_id))
    
    def test_get_pipeline_archive_for_job_raises_error_if_job_not_completed(self):
        self.mock_is_job_completed.return_value = False
        with self.assertRaises(KeyError) as context:
            get_pipeline_archiver_for_job(self.job_id)
        
        self.assertTrue('Model Package ID {} does not exist'.format(self.job_id) in str(context.exception))

    def test_get_pipeline_archive_for_job_calls_is_job_completed_with_correct_arguments(self):
        from foundations_contrib.global_state import redis_connection
        self.mock_is_job_completed.return_value = True
        get_pipeline_archiver_for_job(self.job_id)
        self.mock_is_job_completed.assert_called_with(self.job_id, redis_connection)