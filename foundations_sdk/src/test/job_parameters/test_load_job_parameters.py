"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.job_parameters import load_parameters

class TestLoadJobParameters(Spec):
    
    mock_open = let_patch_mock_with_conditional_return('builtins.open')

    @let
    def mock_parameters(self):
        keys = self.faker.words()
        values = self.faker.words()
        return {key: value for key, value in zip(keys, values)}
        
    @let
    def serialized_mock_parameters(self):
        import json
        return json.dumps(self.mock_parameters)

    mock_file = let_mock()

    @set_up
    def set_up(self):
        self.mock_file.__enter__ = self._mock_file_enter
        self.mock_file.__exit__ = self._mock_exit
        self.mock_file.read.return_value = self.serialized_mock_parameters
        self.mock_open.return_when(self.mock_file, 'foundations_job_parameters.json', 'r')

    def test_can_load_json_parameters(self):
        self.assertEqual(self.mock_parameters, load_parameters())

    def test_is_accessible_globally(self):
        import foundations
        self.assertEqual(load_parameters, foundations.load_parameters)

    def test_returns_default_of_empty_dict_if_file_not_found(self):
        mock_open = self.patch('builtins.open')
        mock_open.side_effect = FileNotFoundError('beep')
        self.assertEqual({}, load_parameters())

    def _mock_file_enter(self, *args, **kwargs):
        return self.mock_file

    def _mock_exit(self, *args, **kwargs):
        pass