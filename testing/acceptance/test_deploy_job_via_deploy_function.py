"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from acceptance.mixins.job_deploy_function_test_scaffold import JobDeployFunctionTestScaffold

import foundations

@skip('We no longer support deploy; pending deletion')
class TestDeployJobViaDeployFunction(Spec, JobDeployFunctionTestScaffold):
    
    def _log_level(self):
        return 'FATAL'

    def _change_foundations_home(self, new_home):
        from foundations_contrib.utils import foundations_home
        import os

        self._old_home = foundations_home()
        os.environ['FOUNDATIONS_HOME'] = new_home

    def _reset_foundations_home(self):
        import os
        os.environ['FOUNDATIONS_HOME'] = self._old_home

    @set_up
    def set_up(self):
        self._old_home = None
        self._set_up()
        self._change_foundations_home(self.temp_home)

    @tear_down
    def tear_down(self):
        self._reset_foundations_home()
        self._tear_down()

    def test_deploy_job_with_all_arguments_specified_deploys_job(self):
        self._test_deploy_job_with_all_arguments_specified_deploys_job()

    def test_deploy_job_with_no_arguments_specified_deploys_job_with_defaults(self):
        self._test_deploy_job_with_no_arguments_specified_deploys_job_with_defaults()

    def _deploy_job_with_defaults(self):
        return self._deploy_job()

    def _deploy_job(self, **kwargs):
        import foundations
        return foundations.deploy(**kwargs)

    def _uuid(self, uuid_container):
        return uuid_container.job_name()