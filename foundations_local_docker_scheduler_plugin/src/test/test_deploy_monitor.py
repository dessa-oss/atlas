"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestDeployMonitor(Spec):

    @let
    def job_name(self):
        return self.faker.uuid4()

    def test_job_bundle_returns_job_bundler_with_correct_params(self):
        from foundations_local_docker_scheduler_plugin.deploy_monitor import job_bundle

        mock_job_bundler_class = self.patch('foundations_contrib.job_bundler.JobBundler', ConditionalReturn())

        mock_empty_job_class = self.patch('foundations_contrib.job_bundling.empty_job.EmptyJob')
        mock_empty_job = Mock()
        mock_empty_job_class.return_value = mock_empty_job

        mock_folder_job_source_bundle_class = self.patch('foundations_contrib.job_bundling.folder_job_source_bundle.FolderJobSourceBundle')
        mock_folder_job_source_bundle = Mock()
        mock_folder_job_source_bundle_class.return_value = mock_folder_job_source_bundle

        mock_config_method = self.patch('foundations_contrib.global_state.config_manager.config')
        mock_config = Mock()
        mock_config_method.return_value = mock_config

        mock_job_bundler = Mock()
        mock_job_bundler_class.return_when(mock_job_bundler, self.job_name, mock_config, mock_empty_job, mock_folder_job_source_bundle, 'job_source')

        self.assertEqual(mock_job_bundler, job_bundle(self.job_name))

        