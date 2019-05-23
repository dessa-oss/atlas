"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

@skip('Not yet ready')
class TestResultsFileCreation(Spec):

    @let
    def result_file_path(self):
        import os

        file_path =  os.path.join(self.results_directory, self.faker.file_path(extension='pkl')[1:])
        return file_path

    @let
    def results_directory(self):
        return self.faker.word()

    @let
    def gcp_uri(self):
        return 'gs://' + self.faker.uri_path()

    @let
    def aws_uri(self):
        return 's3://' + self.faker.uri_path()
    
    def test_job_creates_downloadable_results_files_in_local_file_system(self):
        from foundations.global_state import config_manager

        config_manager['artifact_path'] = self.results_directory
        self._create_job_and_download_results_files()

    def test_job_creates_downloadable_results_files_in_gcp_bucket(self):
        from foundations.global_state import config_manager
        from foundations_gcp.gcp_bucket import GCPBucket
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive


        config_manager['artifact_path'] = self.results_directory
        config_manager['artifact_end_point_implementation'] = {
            'archive_type': BucketPipelineArchive,
            'constructor_arguments': [GCPBucket, self.gcp_uri]
        }
        self._create_job_and_download_results_files()

    def test_job_creates_downloadable_results_files_in_aws(self):
        from foundations.global_state import config_manager
        from foundations_aws.aws_bucket import AWSBucket
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive


        config_manager['artifact_path'] = self.results_directory
        config_manager['artifact_end_point_implementation'] = {
            'archive_type': BucketPipelineArchive,
            'constructor_arguments': [AWSBucket, self.aws_uri]
        }
        self._create_job_and_download_results_files()

    def _create_job_and_download_results_files(self):
        from acceptance.fixtures.stages import save_file_with_pickle
        from foundations.global_state import foundations_context
        import subprocess

        stage = foundations_context.pipeline().stage(save_file_with_pickle, self.result_file_path)
        stage.persist()
        deployment = stage.run()
        deployment.wait_for_deployment_to_complete()

        job_id = deployment.job_name()
        path = 'user_path'
        subdirectory = 'user_subdirectory'
        subprocess.run(['python', '-m', 'foundations', 'retrieve', 'artifacts', '--job-id={}'.format(job_id), '--path={}'.format(path),'--filedir={}'.format(subdirectory)])
