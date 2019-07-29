"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_spec.extensions import let_fake_redis

class TestSyncableDirectory(Spec):

    mock_artifact_file_listing = let_patch_mock_with_conditional_return(
        'foundations_contrib.archiving.upload_artifacts.list_of_files_to_upload_from_artifact_path'
    )
    mock_load_archive = let_patch_mock_with_conditional_return(
        'foundations_contrib.archiving.load_archive'
    )
    mock_mkdtemp = let_patch_mock('tempfile.mkdtemp')
    mock_archive = let_mock()
    mock_redis = let_fake_redis()
    mock_mkdir = let_patch_mock('os.makedirs')
    mock_get_logger = let_patch_mock_with_conditional_return('foundations_contrib.global_state.log_manager.get_logger')
    mock_logger = let_mock()

    @let
    def key(self):
        return self.faker.word()

    @let
    def directory_path(self):
        return self.faker.uri_path()

    @let
    def file_listing_without_directory(self):
        return self.faker.sentences()

    @let
    def file_listing(self):
        return [f'{self.directory_path}/{path}' for path in self.file_listing_without_directory]

    @let
    def stat_mtime_mapping(self):
        return {file_name: self.faker.random.random() * 1000000 for file_name in self.file_listing_without_directory}

    @let
    def stat_mtime_mapping_after_file_change(self):
        import copy

        mapping = copy.deepcopy(self.stat_mtime_mapping)
        key_to_change = list(mapping)[0]
        mapping[key_to_change] += 10

        return mapping

    @let
    def remote_job_id(self):
        return self.faker.uuid4()

    @let
    def local_job_id(self):
        return self.faker.uuid4()

    @let
    def syncable_directory(self):
        from foundations.artifacts.syncable_directory import SyncableDirectory
        return SyncableDirectory(self.key, self.directory_path, self.local_job_id, self.remote_job_id)

    @let
    def syncable_directory_in_uploading_job(self):
        from foundations.artifacts.syncable_directory import SyncableDirectory
        return SyncableDirectory(self.key, self.directory_path, self.local_job_id, self.local_job_id)

    @set_up
    def set_up(self):
        self.patch('foundations_contrib.global_state.redis_connection', self.mock_redis)
        self.mock_artifact_file_listing.return_when(self.file_listing, self.directory_path)
        self.mock_load_archive.return_when(self.mock_archive, 'artifact_archive')
        self.mock_get_logger.return_when(self.mock_logger, 'foundations.artifacts.syncable_directory')

        self.mock_os_stat = self.patch('os.stat', ConditionalReturn())

        for file_name, stat_mtime in self.stat_mtime_mapping.items():
            mock_stat = Mock()
            mock_stat.st_mtime = stat_mtime
            self.mock_os_stat.return_when(mock_stat, f'{self.directory_path}/{file_name}')

    def test_uploads_all_files(self):
        expected_calls = []
        for file in self.file_listing:
            remote_path = file[len(self.directory_path)+1:]
            expected_calls.append(
                call(
                    f'synced_directories/{self.key}', 
                    file, 
                    self.local_job_id,
                    remote_path
                )
            )
        self.syncable_directory.upload()
        self.mock_archive.append_file.assert_has_calls(expected_calls)

    def test_upload_should_log_warning_if_no_local_job_set(self):
        from foundations.artifacts.syncable_directory import SyncableDirectory

        directory = SyncableDirectory(self.key, self.directory_path, None, self.remote_job_id)
        directory.upload()
        self.mock_logger.warning.assert_any_call('local_job_id required for uploading artifacts')
        
        
    def test_upload_does_not_upload_if_no_local_job(self):
        from foundations.artifacts.syncable_directory import SyncableDirectory

        directory = SyncableDirectory(self.key, self.directory_path, None, self.remote_job_id)
        directory.upload()
        self.mock_archive.append_file.assert_not_called()

    def test_tracks_uploaded_files_in_redis(self):
        self.syncable_directory.upload()
        files = self.mock_redis.lrange(f'jobs:{self.local_job_id}:synced_artifacts:{self.key}', 0, -1)
        files = [file.decode() for file in files]
        self.assertEqual(self.file_listing_without_directory, files)

    def test_tracks_uploaded_file_timestamps_in_redis(self):
        self.syncable_directory.upload()
        timestamp_mapping = self.mock_redis.hgetall(f'jobs:{self.local_job_id}:synced_artifacts:{self.key}:timestamps')
        decoded_timestamp_mapping = {file.decode(): float(m_time_from_redis) for file, m_time_from_redis in timestamp_mapping.items()} 
        self.assertEqual(self.stat_mtime_mapping, decoded_timestamp_mapping)

    def test_download_all_files(self):
        expected_calls = []
        for file in self.file_listing:
            self.mock_redis.rpush(f'jobs:{self.remote_job_id}:synced_artifacts:{self.key}', file)
            download_call = call(
                f'synced_directories/{self.key}', 
                file, 
                self.remote_job_id, 
                f'{self.directory_path}/{file}'
            )
            expected_calls.append(download_call)
        self.syncable_directory.download()
        self.mock_archive.fetch_file_path_to_target_file_path.assert_has_calls(expected_calls)        

    def test_download_ensures_paths_exist(self):
        import os.path

        expected_calls = []
        for file in self.file_listing:
            self.mock_redis.rpush(f'jobs:{self.remote_job_id}:synced_artifacts:{self.key}', file)
            dirname = os.path.dirname(f'{self.directory_path}/{file}')
            mkdir_call = call(dirname, exist_ok=True)
            expected_calls.append(mkdir_call)
        self.syncable_directory.download()
        self.mock_mkdir.assert_has_calls(expected_calls)        

    def test_foundations_create_syncable_directory_defaults_to_current_job_for_remote_and_local(self):
        from foundations import create_syncable_directory

        self.patch('foundations_internal.pipeline_context.PipelineContext.file_name', self.local_job_id)
        instance = self._mock_syncable_directory(self.local_job_id)
        self.assertEqual(instance, create_syncable_directory(self.key, self.directory_path))

    def test_foundations_create_syncable_directory_uses_source_job_for_remote(self):
        from foundations import create_syncable_directory

        self.patch('foundations_internal.pipeline_context.PipelineContext.file_name', self.local_job_id)
        instance = self._mock_syncable_directory(self.remote_job_id)
        self.assertEqual(instance, create_syncable_directory(self.key, self.directory_path, self.remote_job_id))        

    def test_foundations_create_syncable_directory_without_any_job_ids(self):
        from foundations import create_syncable_directory

        klass_mock = self.patch('foundations.artifacts.syncable_directory.SyncableDirectory', ConditionalReturn())
        instance = Mock()
        klass_mock.return_when(instance, self.key, self.directory_path, None, None)

        self.assertEqual(instance, create_syncable_directory(self.key, self.directory_path))

    def test_foundations_create_syncable_directory_with_no_directory_creates_temp_directory(self):
        from foundations import create_syncable_directory

        create_syncable_directory(self.key, None, self.remote_job_id)
        self.mock_mkdtemp.assert_called_once()

    def test_path_retuns_correct_synced_directory_path(self):
        self.assertEqual(self.directory_path, str(self.syncable_directory))

    def test_syncable_directory_does_a_download_upon_instantiation(self):
        from foundations import create_syncable_directory

        mock_download = self.patch('foundations.artifacts.syncable_directory.SyncableDirectory.download')
        syncable_directory = create_syncable_directory(self.key, None, self.remote_job_id)
        mock_download.assert_called_once()

    def test_upload_only_changed_file(self):
        self.syncable_directory.upload()
        self.mock_os_stat.clear()
        self.mock_archive.append_file.reset_mock()

        for file_name, stat_mtime in self.stat_mtime_mapping_after_file_change.items():
            mock_stat = Mock()
            mock_stat.st_mtime = stat_mtime
            self.mock_os_stat.return_when(mock_stat, f'{self.directory_path}/{file_name}')
        
        self.syncable_directory.upload()

        remote_path = list(self.stat_mtime_mapping)[0]

        self.mock_archive.append_file.assert_called_once_with(f'synced_directories/{self.key}', f'{self.directory_path}/{remote_path}', self.local_job_id, remote_path)

    def test_upload_file_with_same_name_twice_download_that_file_only_once(self):
        self.syncable_directory_in_uploading_job.upload()
        self.syncable_directory_in_uploading_job.upload()

        self.syncable_directory_in_uploading_job.download()
        self.assertEqual(len(self.file_listing), self.mock_archive.fetch_file_path_to_target_file_path.call_count)

    def _mock_syncable_directory(self, source_job_id):
        klass_mock = self.patch('foundations.artifacts.syncable_directory.SyncableDirectory', ConditionalReturn())
        instance = Mock()
        klass_mock.return_when(instance, self.key, self.directory_path, self.local_job_id, source_job_id)
        return instance