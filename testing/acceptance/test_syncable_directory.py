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
    def deployment_2(self):
        import foundations

        return foundations.deploy(
            project_name='test', 
            env='local', 
            entrypoint='main', 
            job_directory='acceptance/fixtures/syncable_directory_job_again', 
            params={'source_job_id': self.job_id}
        )

    @let
    def deployment_with_diffs(self):
        import foundations

        return foundations.deploy(
            project_name='test', 
            env='local', 
            entrypoint='main', 
            job_directory='acceptance/fixtures/syncable_directory_job_with_diffs', 
            params=None
        )

    @let
    def job_id(self):
        return self.deployment.job_name()

    @let
    def job_id_2(self):
        return self.deployment_2.job_name()

    @let
    def job_id_with_diffs(self):
        return self.deployment_with_diffs.job_name()

    @let
    def temp_directory(self):
        from acceptance.config import ARCHIVE_ROOT
        return f'{ARCHIVE_ROOT}/sync'

    @let
    def first_directory_path(self):
        return f'{self.temp_directory}/results'

    @let
    def second_directory_path(self):
        return f'{self.temp_directory}/metadata'

    @let
    def temporary_syncable_directory(self):
        return foundations.create_syncable_directory('some data', None, self.job_id)

    def first_directory(self, job_id):
        return foundations.create_syncable_directory('some data', self.first_directory_path, job_id)

    def second_directory(self, job_id):
        return foundations.create_syncable_directory('some metadata', self.second_directory_path, job_id)

    @set_up
    def set_up(self):
        from acceptance.cleanup import cleanup
        cleanup()

    def test_can_download_from_synced_directory(self):
        import os

        self.first_directory(self.job_id).download()
        self.assertEqual(['some_data.txt'], os.listdir(self.first_directory_path))

        self.second_directory(self.job_id).download()
        self.assertEqual(['some_metadata.txt'], os.listdir(self.second_directory_path))

    def test_can_download_when_no_synced_directory_specified(self):
        import os

        self.temporary_syncable_directory.download()
        self.assertEqual(['some_data.txt'], os.listdir(str(self.temporary_syncable_directory)))
    
    def test_downloads_upon_instantiation(self):
        import os

        syncable_directory = foundations.create_syncable_directory('some data', None, self.job_id)
        self.assertEqual(['some_data.txt'], os.listdir(str(syncable_directory)))

    def test_can_download_from_one_job_and_upload_same_data_to_another(self):
        import os

        self.first_directory(self.job_id_2).download()
        self.assertEqual(['some_data.txt'], os.listdir(self.first_directory_path))

        self.second_directory(self.job_id_2).download()
        self.assertEqual(['some_metadata.txt'], os.listdir(self.second_directory_path))
    
    def test_uploading_twice_only_uploads_changed_or_new_files(self):
        import os

        synced_directory_path = f'/tmp/foundations_acceptance/archive/{self.job_id_with_diffs}/synced_directories/some data'
        expected_files = ['new_file.txt', 'some_data.txt', 'some_metadata.txt']

        files_with_stats = {file_name: os.stat(f'{synced_directory_path}/{file_name}') for file_name in expected_files}

        with open(f'{synced_directory_path}/time_of_upload.txt', 'r') as time_of_upload_file:
            time_of_upload = float(time_of_upload_file.read())

        for unchanged_file in ['some_data.txt']:
            self.assertLessEqual(abs(files_with_stats[unchanged_file].st_mtime - time_of_upload), 0.5)

        for changed_file in ['new_file.txt', 'some_metadata.txt']:
            self.assertLessEqual(abs(files_with_stats[changed_file].st_mtime - (time_of_upload + 10)), 0.5)