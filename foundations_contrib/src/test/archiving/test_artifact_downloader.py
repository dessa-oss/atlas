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

    @let
    def mock_foundations_files(self):
        return [
            'foundations/a',
            'foundations/b',
            'foundations_contrib/c',
            'foundations_contrib/d',
            'foundations_events/e',
            'foundations_events/f',
            'foundations_internal/g',
            'foundations_internal/h',
            'jobs/i',
            'jobs/j',
            'model_serving/k',
            'model_serving/l',
            'venv/m',
            'venv/n',

            'docker_image_version.sh',
            'download_gui_images.sh',
            'foundations_gui.sh',
            'foundations_main.py',
            'foundations_package_manifest.yaml',
            'foundations_requirements.txt',
            'get_version.sh',
            'job.tgz',
            'run.env',
            'run.sh',

            'p.bin',
            'q.bin',
            'r.config.yaml',
            's.config.yaml',

            'template/t',
            'template/u',
            'foundations_scheduler/v',
            'foundations_scheduler/w',
            'foundations_scheduler_core/v',
            'foundations_scheduler_core/w',
            'foundations_scheduler_deployment/v',
            'foundations_scheduler_deployment/w',
            'foundations_scheduler_plugin/v',
            'foundations_scheduler_plugin/w',
        ]

    def test_downloads_single_file_to_specified_directory(self):
        self._mock_file_list(['path/to/my/file'])
        
        self.artifact_downloader.download_files('', self.download_directory)
        
        self.mock_archiver.fetch_persisted_file.assert_called_with('path/to/my/file', self.download_directory + '/path/to/my/file')

    def test_downloads_multiple_files_to_specified_directory(self):
        self._mock_file_list(['different/file', 'other/different/file'])
        
        self.artifact_downloader.download_files('', self.download_directory)
        
        first_file_download = call('different/file', self.download_directory + '/different/file')
        second_file_download = call('other/different/file', self.download_directory + '/other/different/file')
        self.mock_archiver.fetch_persisted_file.assert_has_calls([first_file_download, second_file_download])

    def test_ensures_target_directory_exists(self):
        self._mock_file_list(['path/to/my/file'])
        
        self.artifact_downloader.download_files('', self.download_directory)
        self.make_directory_mock.assert_called_with(self.download_directory + '/path/to/my', exist_ok=True)

    def test_downloads_multiple_files_to_specified_directory(self):
        self._mock_file_list(['different/file', 'other/different/file'])
        
        self.artifact_downloader.download_files('', self.download_directory)
        
        first_dirctory_creation = call(self.download_directory + '/different', exist_ok=True)
        second_dirctory_creation = call(self.download_directory + '/other/different', exist_ok=True)
        self.make_directory_mock.assert_has_calls([first_dirctory_creation, second_dirctory_creation])

    def test_downloads_only_files_with_specified_source_directory(self):
        self._mock_file_list(['different/file', 'other/different/file'])
        
        self.artifact_downloader.download_files('other/', self.download_directory)
        self.mock_archiver.fetch_persisted_file.assert_called_once_with('other/different/file', self.download_directory + '/other/different/file')

    def test_downloads_only_files_with_specified_source_directory_with_different_source_directory(self):
        self._mock_file_list(['different/file', 'other/different/file'])
        
        self.artifact_downloader.download_files('different/', self.download_directory)
        self.mock_archiver.fetch_persisted_file.assert_called_once_with('different/file', self.download_directory + '/different/file')

    def test_download_does_not_include_foundations_files(self):
        for foundations_file in self.mock_foundations_files:
            self._mock_file_list(['path/to/some/file', foundations_file])
            
            self.artifact_downloader.download_files('', self.download_directory)
            self.mock_archiver.fetch_persisted_file.assert_called_with('path/to/some/file', self.download_directory + '/path/to/some/file') 

    def _mock_file_list(self, file_list):
        self.mock_archiver.fetch_miscellaneous = ConditionalReturn()
        self.mock_archiver.fetch_miscellaneous.return_when(file_list, 'job_artifact_listing.pkl')        