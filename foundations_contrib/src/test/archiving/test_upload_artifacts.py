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

    @let
    def fake_path(self):
        return self.faker.uri_path()

    @let
    def fake_list_of_tuples(self):
        return [
            ('parent_dir', ['child_dir1', 'child_dir2'], ['file1']),
            ('parent_dir/child_dir1', [], ['file2', 'file3']),
            ('parent_dir/child_dir2', ['child_dir3'], ['file4']),
            ('parent_dir/child_dir2/child_dir3', [], ['file5'])
        ]

    @set_up
    def  set_up(self):
        self.mock_os_walk.return_value = iter(self.fake_list_of_tuples)

    def test_upload_artifacts_crawls_artifact_path(self):
        upload_artifacts()
        self.mock_artifact_path_crawl.assert_called()

    def test_upload_artifacts_passes_generator_from_artifact_path_crawls_to_file_names_for_artifact(self):
        mock_generator = Mock()
        self.mock_artifact_path_crawl.return_value = mock_generator
        upload_artifacts()
        self.mock_file_names_for_artifacts_path.assert_called_with(mock_generator)
