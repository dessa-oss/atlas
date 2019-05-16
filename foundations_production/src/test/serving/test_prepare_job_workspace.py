"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *

from foundations_production.serving import prepare_job_workspace

class TestPrepareJobWorkspace(Spec):
    
    mock_extract_job_source = let_patch_mock('foundations_production.serving.extract_job_source')
    mock_chdir = let_patch_mock('os.chdir')

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def workspace_directory(self):
        return '/tmp/foundations_workspaces/{}'.format(self.job_id)

    @set_up
    def set_up(self):
        self._extract_job_source_called = False
        self._chdir_called = False

        self.mock_extract_job_source.side_effect = self._set_extract_job_source_called
        self.mock_chdir.side_effect = self._check_extract_job_source_called_and_set_chdir_called

    def test_prepare_job_workspace_creates_job_workspace(self):
        prepare_job_workspace(self.job_id)
        self.mock_extract_job_source.assert_called_with(self.job_id)

    def test_prepare_job_workspace_changes_directory_to_workspace_directory(self):
        prepare_job_workspace(self.job_id)
        self.mock_chdir.assert_called_with(self.workspace_directory)

    def test_prepare_job_workspace_adds_workspace_directory_to_python_path(self):
        mock_sys_path = self.patch('sys.path')

        prepare_job_workspace(self.job_id)
        mock_sys_path.append.assert_called_with(self.workspace_directory)

    def _set_extract_job_source_called(self, *args):
        self._extract_job_source_called = True

    def _check_extract_job_source_called_and_set_chdir_called(self, *args):
        if not self._extract_job_source_called:
            raise AssertionError('Job workspace needs to be created before directory changed')
        self._chdir_called = True

    def _check_chdir_called(self, *args):
        if not self._chdir_called:
            raise AssertionError('Directory needs to be changed before predictor created')