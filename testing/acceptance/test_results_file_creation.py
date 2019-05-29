"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *


class TestResultsFileCreation(Spec):

    @let
    def random_subdirectory_for_model(self):
        import os

        return os.path.join('model', self.faker.uri_path())

    @let
    def random_subdirectory_for_metrics(self):
        import os

        return os.path.join('metrics', self.faker.uri_path())

    @let
    def model_artifact_file_relative_path(self):
        import os

        return os.path.join(self.random_subdirectory_for_model, self.faker.file_path(extension='pkl')[1:])

    @let
    def metrics_artifact_file_relative_path(self):
        import os

        return os.path.join(self.random_subdirectory_for_metrics, self.faker.file_path(extension='pkl')[1:])

    @let
    def remote_artifacts_directory(self):
        return self.faker.word()

    @let
    def model_remote_artifact_file_path(self):
        import os

        return os.path.join(self.remote_artifacts_directory, self.model_artifact_file_relative_path)

    @let
    def metrics_remote_artifact_file_path(self):
        import os

        return os.path.join(self.remote_artifacts_directory, self.metrics_artifact_file_relative_path)

    @let
    def save_path(self):
        import os

        return os.path.join('/tmp', self.faker.uri_path())

    @let
    def model_local_save_artifact_file_path(self):
        import os

        return os.path.join(self.save_path, self.model_artifact_file_relative_path)

    @let
    def metrics_local_save_artifact__file_path(self):
        import os

        return os.path.join(self.save_path, self.metrics_artifact_file_relative_path)

    @let
    def gcp_uri(self):
        return 'gs://' + self.faker.uri_path()

    @let
    def aws_uri(self):
        return 's3://' + self.faker.uri_path()

    class EmptyClass(object):
            pass

    @skip('Not yet ready, in process')
    def test_job_creates_downloadable_results_files_in_local_file_system(self):
        from foundations.global_state import config_manager

        config_manager['artifact_path'] = self.save_path
        self._create_job_and_download_results_files()

    @skip('Not yet ready, not a priority')
    def test_job_creates_downloadable_results_files_in_gcp_bucket(self):
        from foundations.global_state import config_manager
        from foundations_gcp.gcp_bucket import GCPBucket
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive


        config_manager['artifact_path'] = self.save_path
        config_manager['artifact_end_point_implementation'] = {
            'archive_type': BucketPipelineArchive,
            'constructor_arguments': [GCPBucket, self.gcp_uri]
        }
        self._create_job_and_download_results_files()

    @skip('Not yet ready, not a priority')
    def test_job_creates_downloadable_results_files_in_aws(self):
        from foundations.global_state import config_manager
        from foundations_aws.aws_bucket import AWSBucket
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive


        config_manager['artifact_path'] = self.save_path
        config_manager['artifact_end_point_implementation'] = {
            'archive_type': BucketPipelineArchive,
            'constructor_arguments': [AWSBucket, self.aws_uri]
        }
        self._create_job_and_download_results_files()

    def _create_job_and_download_results_files(self):
        from acceptance.fixtures.stages import save_file_with_pickle
        from foundations import create_stage
        import shutil

        empty_class_instance_1 = self.EmptyClass()

        model_stage = create_stage(save_file_with_pickle)
        metrics_stage = create_stage(save_file_with_pickle)
        empty_class_instance_2 = model_stage(self.model_remote_artifact_file_path, empty_class_instance_1)
        empty_class_instance_3 = metrics_stage(self.metrics_remote_artifact_file_path, empty_class_instance_2)
        deployment = empty_class_instance_3.run()
        deployment.wait_for_deployment_to_complete()

        job_id = deployment.job_name()
        self._run_retrieve_cli_command(job_id)
        self.assertCountEqual(self._fully_expanded_paths_for_downloads(), [self.model_local_save_artifact_file_path, self.metrics_local_save_artifact__file_path])
        shutil.rmtree(save_dir)
        self._run_retrieve_cli_command(job_id, source_dir=self.random_subdirectory_for_model)
        self.assertCountEqual(self._fully_expanded_paths_for_downloads(), [self.model_local_save_artifact_file_path])
        shutil.rmtree(save_dir)
        self._run_retrieve_cli_command(job_id, source_dir=self.random_subdirectory_for_metrics)
        self.assertCountEqual(self._fully_expanded_paths_for_downloads(), [self.metrics_local_save_artifact__file_path])
        shutil.rmtree(save_dir)

    def _fully_expanded_paths_for_downloads(self):
        import os

        result = []
        for root, dirs, files in os.walk(self.save_path):
            if files:
                result += [os.path.join(root, file) for file in files]
            elif not dirs:
                result.append(root)
        return result

    def _run_retrieve_cli_command(self, job_id, source_dir=None):
        import subprocess

        cmd_line = ['python', '-m', 'foundations', 'retrieve', 'artifacts', '--job_id={}'.format(job_id), '--save_dir={}'.format(self.save_path)]
        if source_dir:
            cmd_line.append(' --source_dir={}'.format(source_dir))
        subprocess.run(cmd_line, check=True)
