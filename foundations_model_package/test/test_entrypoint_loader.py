"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.entrypoint_loader import EntrypointLoader

class TestEntrypointLoader(Spec):

    path_exists = let_patch_mock_with_conditional_return('os.path.exists')

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def job_root(self):
        return self.faker.file_path()

    @let
    def job(self):
        job = Mock()
        job.id.return_value = self.job_id
        job.root.return_value = self.job_root
        
        return job

    @set_up
    def set_up(self):
        self.path_exists.return_when(True, self.job_root)

    def test_entrypoint_loader_checks_for_job_root_and_complains_if_it_does_not_exist(self):
        self.path_exists.clear()
        self.path_exists.return_when(False, self.job_root)

        with self.assertRaises(Exception) as error_context:
            EntrypointLoader(self.job).entrypoint_function()

        self.assertIn(f'Job {self.job_id} not found!', error_context.exception.args)