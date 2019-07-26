"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import foundations

class TestSyncableDirectory(Spec):

    @let
    def deployment(self):
        import foundations

        return foundations.deploy(
            project_name='test', 
            env='local', 
            entrypoint='main', 
            job_directory='acceptance/fixtures/syncable_directory_job', 
            params=None
        )

    @let
    def job_id(self):
        return self.deployment.job_name()

    @let
    def temp_directory(self):
        from acceptance.config import ARCHIVE_ROOT
        return f'{ARCHIVE_ROOT}/sync'

    @let
    def first_directory_path(self):
        return f'{self.temp_directory}/results'

    @let
    def first_directory(self):
        return foundations.create_syncable_directory('some data', self.first_directory_path, self.job_id)

    @let
    def second_directory_path(self):
        return f'{self.temp_directory}/metadata'

    @let
    def second_directory(self):
        return foundations.create_syncable_directory('some metadata', self.second_directory_path, self.job_id)

    @let
    def temporary_syncable_directory(self):
        return foundations.create_syncable_directory('some data', None, self.job_id)

    @set_up
    def set_up(self):
        from acceptance.cleanup import cleanup
        cleanup()

    def test_can_download_from_synced_directory(self):
        import os

        self.first_directory.download()
        self.assertEqual(['some_data.txt'], os.listdir(self.first_directory_path))

        self.second_directory.download()
        self.assertEqual(['some_metadata.txt'], os.listdir(self.second_directory_path))

    def test_can_download_when_no_synced_directory_specified(self):
        import os

        self.temporary_syncable_directory.download()
        self.assertEqual(['some_data.txt'], os.listdir(f'{self.temporary_syncable_directory.path()}'))
    