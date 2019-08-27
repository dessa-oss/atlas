"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_contrib.cli.job_submission.submit_job import submit

class TestJobSubmissionSubmit(Spec):
    
    mock_arguments = let_mock()
    mock_load_config = let_patch_mock('foundations_contrib.cli.job_submission.config.load')
    mock_os_chdir = let_patch_mock('os.chdir')
    mock_os_getcwd = let_patch_mock('os.getcwd')

    @let
    def scheduler_config(self):
        return self.faker.name()

    @let
    def current_directory(self):
        return self.faker.uri_path()
        
    @let
    def job_directory(self):
        return self.faker.uri_path()

    @set_up
    def set_up(self):
        self.mock_arguments.scheduler_config = None
        self.mock_arguments.job_dir = None
        self.mock_arguments.project_name = None
        
        self.mock_os_getcwd.return_value = self.current_directory

    def test_loads_default_scheduler_config(self):
        submit(self.mock_arguments)
        self.mock_load_config.assert_called_with('scheduler')

    def test_loads_specific_scheduler_config(self):
        self.mock_arguments.scheduler_config = self.scheduler_config
        submit(self.mock_arguments)
        self.mock_load_config.assert_called_with(self.scheduler_config)

    def test_runs_in_job_directory_when_specified(self):
        self.mock_arguments.job_dir = self.job_directory
        submit(self.mock_arguments)
        self.mock_os_chdir.assert_has_calls([call(self.job_directory), call(self.current_directory)])

    def test_runs_in_current_directory_when_no_job_dir_specified(self):
        submit(self.mock_arguments)
        self.mock_os_chdir.assert_has_calls([call(self.current_directory), call(self.current_directory)])
