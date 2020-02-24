
from foundations_spec import *
import foundations
from acceptance.mixins.run_local_job import RunLocalJob

class TestSyncableDirectory(Spec, RunLocalJob):

    @set_up
    def set_up(self):
        from acceptance.cleanup import cleanup
        cleanup()
    
    def run_job(self):
        self._run_job_file('acceptance/fixtures/syncable_directory_job', job_id=self.job_id_1, entrypoint='main.py')

    def run_job_2(self):
        self._run_job_file('acceptance/fixtures/syncable_directory_job_again', job_id=self.job_id_2, entrypoint='main.py')

    def run_job_with_diffs(self):
        self._run_job_file('acceptance/fixtures/syncable_directory_job_with_diffs', job_id=self.job_id_with_diffs, entrypoint='main.py')

    def run_job_multiple_files(self):
        self._run_job_file('acceptance/fixtures/syncable_directory_job_multiple_files', job_id=self.job_id_multiple_files, entrypoint='main.py')

    @let
    def job_id_1(self):
        return self.faker.uuid4()

    @let
    def job_id_2(self):
        return self.faker.uuid4()

    @let
    def job_id_with_diffs(self):
        return self.faker.uuid4()

    @let
    def job_id_multiple_files(self):
        return self.faker.uuid4()

    @let
    def temp_directory(self):
        from tempfile import mkdtemp
        return mkdtemp()

    @let
    def first_directory_path(self):
        return f'{self.temp_directory}/results'

    @let
    def second_directory_path(self):
        return f'{self.temp_directory}/metadata'

    def temporary_syncable_directory(self, job_id):
        return foundations.create_syncable_directory('some data', None, job_id)

    def first_directory(self, job_id):
        return foundations.create_syncable_directory('some data', self.first_directory_path, job_id)

    def second_directory(self, job_id):
        return foundations.create_syncable_directory('some metadata', self.second_directory_path, job_id)

    def test_can_download_from_synced_directory(self):
        import os

        self.run_job()

        self.first_directory(self.job_id_1).download()
        self.assertEqual(['some_data.txt'], os.listdir(self.first_directory_path))

        self.second_directory(self.job_id_1).download()
        self.assertEqual(['some_metadata.txt'], os.listdir(self.second_directory_path))

    def test_can_download_when_no_synced_directory_specified(self):
        import os

        self.run_job()

        sync_dir = self.temporary_syncable_directory(self.job_id_1)
        sync_dir.download()

        self.assertEqual(['some_data.txt'], os.listdir(str(sync_dir)))
    
    def test_downloads_upon_instantiation(self):
        import os

        self._deploy_job_file('acceptance/fixtures/syncable_directory_job', job_id=self.job_id_1, entrypoint='main.py')
        syncable_directory = foundations.create_syncable_directory('some data', None, self.job_id_1)
        self.assertEqual(['some_data.txt'], os.listdir(str(syncable_directory)))

    def test_can_download_from_one_job_and_upload_same_data_to_another(self):
        import os
        import json

        self.run_job()

        with open('acceptance/fixtures/syncable_directory_job_again/foundations_job_parameters.json', 'w') as params_file:
            json.dump({'source_job_id': self.job_id_1}, params_file)

        self.run_job_2()

        syncable_directory_data = foundations.create_syncable_directory('some data', self.first_directory_path, source_job_id=self.job_id_2)
        syncable_directory_data.download()
        self.assertEqual(['some_data.txt'], os.listdir(self.first_directory_path))

        syncable_directory_meta = foundations.create_syncable_directory('some metadata', self.second_directory_path, source_job_id=self.job_id_2)
        syncable_directory_meta.download()
        self.assertEqual(['some_metadata.txt'], os.listdir(self.second_directory_path))
    
    def test_uploading_twice_only_uploads_changed_or_new_files(self):
        import os
        from foundations_contrib.global_state import config_manager

        self.run_job_with_diffs()
        synced_directory_path = f'/tmp/foundations_acceptance/archive/{self.job_id_with_diffs}/synced_directories/some data'
        expected_files = ['new_file.txt', 'some_data.txt', 'some_metadata.txt']

        files_with_stats = {file_name: os.stat(f'{synced_directory_path}/{file_name}') for file_name in expected_files}

        with open(f'{synced_directory_path}/time_of_upload.txt', 'r') as time_of_upload_file:
            time_of_upload = float(time_of_upload_file.read())

        for unchanged_file in ['some_data.txt']:
            self.assertLessEqual(abs(files_with_stats[unchanged_file].st_mtime - time_of_upload), 0.5)

        for changed_file in ['new_file.txt', 'some_metadata.txt']:
            self.assertLessEqual(abs(files_with_stats[changed_file].st_mtime - (time_of_upload + 10)), 0.5)

    def test_downloading_twice_upserts_if_newer_files_available_and_leaves_unchanged_files_alone(self):
        import os
        import shutil
        import time
        from tempfile import mkdtemp
        import foundations
        from foundations.artifacts.syncable_directory import SyncableDirectory

        SLEEP_TIME = 1

        self._run_job_file('acceptance/fixtures/syncable_directory_job_multiple_files', job_id=self.job_id_multiple_files, entrypoint='main.py')

        local_syncable_directory = SyncableDirectory('some data', self.first_directory_path, self.job_id_multiple_files, self.job_id_multiple_files)
        local_syncable_directory.download()
        self.assertEqual(sorted(['some_data_for_multiple_files.txt', 'some_metadata.txt']), sorted(os.listdir(self.first_directory_path)))
        
        time_of_download = time.time()
        temp_workspace = mkdtemp()

        hack_directory = SyncableDirectory('some data', temp_workspace, self.job_id_multiple_files, self.job_id_multiple_files)
        os.remove(f'{temp_workspace}/some_data_for_multiple_files.txt')
        
        time.sleep(SLEEP_TIME)

        with open(f'{temp_workspace}/some_metadata.txt', 'w') as metadata_file:
            metadata_file.write('some new metadata i guess')

        with open(f'{temp_workspace}/new_file.txt', 'w') as new_file:
            new_file.write('i am a new file')

        hack_directory.upload()

        local_syncable_directory.download()

        expected_files = ['some_metadata.txt', 'some_data_for_multiple_files.txt',  'new_file.txt']
        files_with_stats = {file_name: os.stat(f'{local_syncable_directory}/{file_name}') for file_name in expected_files}
        self.assertEqual(sorted(expected_files), sorted(os.listdir(self.first_directory_path)))

        try:
            for unchanged_file in ['some_data_for_multiple_files.txt']:
                self.assertLessEqual(abs(files_with_stats[unchanged_file].st_mtime - time_of_download), 0.5)

            for changed_file in ['new_file.txt', 'some_metadata.txt']:
                self.assertLessEqual(abs(files_with_stats[changed_file].st_mtime - (time_of_download + SLEEP_TIME)), 0.5)
        finally:
            shutil.rmtree(temp_workspace, ignore_errors=True)
