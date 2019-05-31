"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.archiving.upload_artifacts import upload_artifacts


class TestUploadArtifacts(Spec):

    mock_os_walk = let_patch_mock('os.walk', ConditionalReturn())
    mock_artifact_path_crawl = let_patch_mock('foundations_contrib.archiving.artifact_path_crawl.artifact_path_crawl')
    mock_file_names_for_artifacts_path = let_patch_mock('foundations_contrib.archiving.file_names_for_artifacts_path.file_names_for_artifacts_path')
    mock_open = let_patch_mock('builtins.open')    
    pipeline_archiver = let_mock()
    
    @let_now
    def mock_get_pipeline_archiver_for_job(self):
        mock = self.patch('foundations_contrib.archiving.get_pipeline_archiver_for_job', ConditionalReturn())
        mock.return_when(self.pipeline_archiver, self.fake_job_id)
        return mock
    
    class MockFile(Mock):

        def __enter__(self):
            return self
    
        def __exit__(self, *arg, **kwargs):
            pass

    @let
    def fake_path(self):
        return self.faker.uri_path()

    @let
    def fake_job_id(self):
        return self.faker.uuid4()

    @let
    def fake_list_of_tuples(self):
        return [
            ('parent_dir', ['child_dir1', 'child_dir2'], ['file1']),
            ('parent_dir/child_dir1', [], ['file2', 'file3']),
            ('parent_dir/child_dir2', ['child_dir3'], ['file4']),
            ('parent_dir/child_dir2/child_dir3', [], ['file5'])
        ]

    @let
    def fake_list_of_files(self):
        return [
            'parent_dir/file1', 
            'parent_dir/child_dir1/file2',
            'parent_dir/child_dir1/file3',
            'parent_dir/child_dir2/file4',
            'parent_dir/child_dir2/child_dir3/file5'
            ]

    @set_up
    def  set_up(self):
        self.mock_os_walk.return_value = iter(self.fake_list_of_tuples)
        self.mock_listing_file = self.MockFile()
        self.mock_open.return_value = self.mock_listing_file
        self.mock_file_names_for_artifacts_path.return_value = iter(self.fake_list_of_files)

    def test_upload_artifacts_crawls_artifact_path(self):
        upload_artifacts(self.fake_job_id)
        self.mock_artifact_path_crawl.assert_called()

    def test_upload_artifacts_passes_generator_from_artifact_path_crawls_to_file_names_for_artifact(self):
        mock_generator = Mock()
        self.mock_artifact_path_crawl.return_value = mock_generator
        upload_artifacts(self.fake_job_id)
        self.mock_file_names_for_artifacts_path.assert_called_with(mock_generator)

    def test_upload_artifacts_writes_files_to_listing_file(self):
        upload_artifacts(self.fake_job_id)
        self.pipeline_archiver.append_miscellaneous.assert_called_with('job_artifact_listing.pkl', self.fake_list_of_files)        

    def test_upload_artifacts_calls_get_pipeline_archiver_for_job(self):
        upload_artifacts(self.fake_job_id)
        self.mock_get_pipeline_archiver_for_job.assert_called_with(self.fake_job_id)

    def test_upload_artifacts_uploads_files_to_pipeline_archiver(self):
        from unittest.mock import call

        upload_artifacts(self.fake_job_id)
        upload_calls = [
            call('parent_dir/file1', 'parent_dir/file1'),
            call('parent_dir/child_dir1/file2', 'parent_dir/child_dir1/file2'),
            call('parent_dir/child_dir1/file3', 'parent_dir/child_dir1/file3'),
            call('parent_dir/child_dir2/file4', 'parent_dir/child_dir2/file4'),
            call('parent_dir/child_dir2/child_dir3/file5', 'parent_dir/child_dir2/child_dir3/file5')
        ]
        self.pipeline_archiver.append_persisted_file.assert_has_calls(upload_calls)