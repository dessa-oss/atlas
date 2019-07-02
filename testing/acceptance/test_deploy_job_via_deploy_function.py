"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from acceptance.mixins.job_deploy_function_test_scaffold import JobDeployFunctionTestScaffold

import foundations

class TestDeployJobViaDeployFunction(Spec, JobDeployFunctionTestScaffold):
    
    def _log_level(self):
        return 'FATAL'

    @set_up
    def set_up(self):
        self._set_up()

    @tear_down
    def tear_down(self):
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