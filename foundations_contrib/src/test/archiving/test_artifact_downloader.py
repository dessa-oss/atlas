"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from unittest.mock import call

class TestArtifactDownloader(Spec):
    
    mock_archiver = let_mock()

    make_directory_mock = let_patch_mock('os.makedirs')

    @let
    def source_directory(self):
        return self.faker.uri_path()

    @let
    def download_directory(self):
        return self.faker.uri_path()

    @let
    def artifact_downloader(self):
        from foundations_contrib.archiving.artifact_downloader import ArtifactDownloader
        return ArtifactDownloader(self.mock_archiver)

    def test_downloads_single_file_to_specified_directory(self):
        file_list = ['path/to/my/file']
        self.mock_archiver.fetch_miscellaneous = ConditionalReturn()
        self.mock_archiver.fetch_miscellaneous.return_when(file_list, 'job_artifact_listing.pkl')
        
        self.artifact_downloader.download_files('', self.download_directory)
        
        self.mock_archiver.fetch_persisted_file.assert_called_with('path/to/my/file', self.download_directory + '/path/to/my/file')

    def test_downloads_multiple_files_to_specified_directory(self):
        file_list = ['different/file', 'other/different/file']
        self.mock_archiver.fetch_miscellaneous = ConditionalReturn()
        self.mock_archiver.fetch_miscellaneous.return_when(file_list, 'job_artifact_listing.pkl')
        
        self.artifact_downloader.download_files('', self.download_directory)
        
        first_file_download = call('different/file', self.download_directory + '/different/file')
        second_file_download = call('other/different/file', self.download_directory + '/other/different/file')
        self.mock_archiver.fetch_persisted_file.assert_has_calls([first_file_download, second_file_download])

    def test_ensures_target_directory_exists(self):
        file_list = ['path/to/my/file']
        self.mock_archiver.fetch_miscellaneous = ConditionalReturn()
        self.mock_archiver.fetch_miscellaneous.return_when(file_list, 'job_artifact_listing.pkl')
        
        self.artifact_downloader.download_files('', self.download_directory)
        
        self.make_directory_mock.assert_called_with(self.download_directory + '/path/to/my', exist_ok=True)

    def test_downloads_multiple_files_to_specified_directory(self):
        file_list = ['different/file', 'other/different/file']
        self.mock_archiver.fetch_miscellaneous = ConditionalReturn()
        self.mock_archiver.fetch_miscellaneous.return_when(file_list, 'job_artifact_listing.pkl')
        
        self.artifact_downloader.download_files('', self.download_directory)
        
        first_dirctory_creation = call(self.download_directory + '/different', exist_ok=True)
        second_dirctory_creation = call(self.download_directory + '/other/different', exist_ok=True)
        self.make_directory_mock.assert_has_calls([first_dirctory_creation, second_dirctory_creation])
