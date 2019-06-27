"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations.deploy import deploy

class TestDeploy(Spec):

    @let_now
    def fake_cwd(self):
        cwd_path = self.faker.file_path()
        patched_os_getcwd = self.patch('os.getcwd')
        patched_os_getcwd.return_value = cwd_path
        return cwd_path

    @let
    def project_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import current_foundations_context
        self._old_project_name = current_foundations_context().project_name()

    @tear_down
    def tear_down(self):
        from foundations_contrib.global_state import current_foundations_context
        current_foundations_context().set_project_name(self._old_project_name)

    def test_deploy_with_defaults_sets_project_name_to_cwd_basename(self):
        import os.path as path

        cwd_name = path.basename(self.fake_cwd)
        self._test_deploy_correctly_sets_project_name(cwd_name)

    def test_deploy_with_project_name_specified_sets_project_name_to_project_name(self):
        self._test_deploy_correctly_sets_project_name(self.project_name, project_name=self.project_name)

    def _test_deploy_correctly_sets_project_name(self, expected_project_name, **kwargs):
        from foundations_contrib.global_state import current_foundations_context

        deploy(**kwargs)
        self.assertEqual(expected_project_name, current_foundations_context().project_name())