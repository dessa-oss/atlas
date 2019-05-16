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

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def workspace_directory(self):
        return '/tmp/foundations_workspaces/{}'.format(self.job_id)

    @set_up
    def set_up(self):
        self._extract_job_source_called = False

    def test_prepare_job_workspace_creates_job_workspace(self):
        prepare_job_workspace(self.job_id)
        self.mock_extract_job_source.assert_called_with(self.job_id)

    def test_prepare_job_workspace_adds_workspace_directory_to_python_path(self):
        mock_sys_path = self.patch('sys.path')

        prepare_job_workspace(self.job_id)
        mock_sys_path.append.assert_called_with(self.workspace_directory)