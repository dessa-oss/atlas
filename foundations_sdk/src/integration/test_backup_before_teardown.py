"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from mock import Mock
from foundations_spec import *
from foundations import BackupBeforeTeardown

@skip
class TestBackupBeforeTearDown(Spec):

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import config_manager
        from foundations_gcp.gcp_bucket import GCPBucket
        import shutil

        list_of_backup_files = ['backup_file.txt', 'backup_file2.txt']

        job_artifact_path = f'{self.artifact_path}/some_job/'
        shutil.rmtree(job_artifact_path, ignore_errors=True)
        shutil.copytree('integration/fixtures/backup_files', job_artifact_path)

    @let
    def destination_path(self):
        return '{0}/{1}'.format(self.artifact_path, self.result_path)
    
    @let
    def artifact_path(self):
        from foundations_contrib.global_state import config_manager
        return config_manager['artifact_archive_implementation']['constructor_arguments'][0]

    @let
    def result_path(self):
        return 'tests/back-up-archive'

    @let
    def gcp_bucket_name(self):
        return 'foundations-testing-bucket'

    @let
    def gcp_bucket(self):
        from foundations_gcp.gcp_bucket import GCPBucket
        return GCPBucket('foundations-testing-bucket')

    def test_backs_up_all_files_from_archive_to_gcp_bucket(self):

        backup_util = BackupBeforeTeardown()
        backup_util.upload_to_gcp(self.result_path, self.gcp_bucket_name)

        list_files = list(self.gcp_bucket.list_files(f'{self.result_path}/archive/some_job/*'))

        expected_files = [
            'tests/back-up-archive/archive/some_job/backup_file.txt', 
            'tests/back-up-archive/archive/some_job/backup_file2.txt'
        ]
        self.assertEqual(expected_files, list_files)
        