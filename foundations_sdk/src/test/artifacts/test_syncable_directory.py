"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestSyncableDirectory(Spec):

    mock_artifact_file_listing = let_patch_mock_with_conditional_return(
        'foundations_contrib.archiving.upload_artifacts.list_of_files_to_upload_from_artifact_path'
    )
    mock_load_archive = let_patch_mock_with_conditional_return(
        'foundations_contrib.archiving.load_archive'
    )
    mock_archive = let_mock()

    @let
    def key(self):
        return self.faker.word()

    @let
    def directory_path(self):
        return self.faker.uri_path()

    @let
    def file_listing(self):
        return [f'{self.directory_path}/{path}' for path in  self.faker.sentences()]

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

    @set_up
    def set_up(self):
        self.mock_artifact_file_listing.return_when(self.file_listing, self.directory_path)
        self.mock_load_archive.return_when(self.mock_archive, 'artifact_archive')

    def test_uploads_all_files(self):
        expected_calls = []
        for file in self.file_listing:
            expected_calls.append(call(f'synced_directories/{self.key}', file, self.local_job_id))
        self.syncable_directory.upload()
        self.mock_archive.append_file.assert_has_calls(expected_calls)