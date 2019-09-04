"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.local_run.initialize_default_environment import create_config_file

class TestInitializeDefaultEnvironment(Spec):

    mock_open = let_patch_mock_with_conditional_return('builtins.open')
    mock_mkdirs = let_patch_mock('os.makedirs')

    @let
    def mock_file(self):
        mock_file = Mock()
        mock_file.__enter__ = lambda *_: mock_file
        mock_file.__exit__ = Mock()
        mock_file.write = self._write_file_data
        return mock_file

    @set_up
    def set_up(self):
        self.mock_open.return_when(self.mock_file, 'config/execution/default.config.yaml', 'w+')
        self._file_data = None

    def test_create_default_config_creates_default_execution_config(self):
        import yaml

        create_config_file()
        config = yaml.load(self._file_data)
        self.assertEqual({'results_config': {}, 'cache_config': {}}, config)

    def test_ensure_directory_exists(self):
        create_config_file()
        self.mock_mkdirs.assert_called_with('config/execution', exist_ok=True)

    def _write_file_data(self, data):
        self._file_data = data

