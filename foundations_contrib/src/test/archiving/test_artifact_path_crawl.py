"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from foundations_contrib.archiving.artifact_path_crawl import artifact_path_crawl

class TestArtifactPathCrawl(Spec):

    mock_config_manager = let_patch_mock('foundations_contrib.global_state.config_manager')
    mock_os_walk = let_patch_mock('os.walk', ConditionalReturn())

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

    @let
    def fake_default_return_for_walk(self):
        return [('results', [], ['default_result.pkl'])]

    @set_up
    def set_up(self):
        self.mock_config_manager.config.return_value = {'artifact_path': self.fake_path}
        self.mock_os_walk.return_when(iter(self.fake_list_of_tuples), self.fake_path)
        self.mock_os_walk.return_when(iter(self.fake_default_return_for_walk), 'results')

    def test_artifact_path_crawler_calls_os_walk_with_default_artifact_path(self):
        self.mock_config_manager.__getitem__.return_value = 'results'
        list(artifact_path_crawl())
        self.mock_os_walk.assert_called_with('results')

    def test_artifact_path_crawler_returns_os_walk_default_walk_if_called_with_artifact_path(self):
        self.mock_config_manager.__getitem__.return_value = 'results'
        self.assertEqual(self.fake_default_return_for_walk, list(artifact_path_crawl()))

    def test_artifact_path_crawler_calls_os_walk_with_artifact_path(self):
        self.mock_config_manager.__getitem__.return_value = self.fake_path
        list(artifact_path_crawl())
        self.mock_os_walk.assert_called_with(self.fake_path)

    def test_artifact_path_crawler_returns_os_walk_default_walk_if_called_with_artifact_path(self):
        self.mock_config_manager.__getitem__.return_value = self.fake_path
        self.assertEqual(self.fake_list_of_tuples, list(artifact_path_crawl()))
