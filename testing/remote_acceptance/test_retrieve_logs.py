"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_spec.helpers import set_up, tear_down
from foundations_spec.helpers.spec import Spec
from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
from foundations import config_manager

class TestRetrieveLogs(Spec):
    
    @set_up
    def set_up(self):
        from foundations import config_manager

        import remote_acceptance.config.remote_config as remote_config

        remote_config.config()

        config_manager['deployment_implementation'] = {
            'deployment_type': SFTPJobDeployment
        }
    
    def test_get_log_returns_log_as_string(self):
        import time
        import foundations

        from remote_acceptance.fixtures.stages import function_that_prints

        function_that_prints = foundations.create_stage(function_that_prints)
        function_that_prints_deployment_object = function_that_prints().run()
        function_that_prints_deployment_object.wait_for_deployment_to_complete(15)

        job_id = function_that_prints_deployment_object.job_name()
        self.assertIn("I am a function. I print things", function_that_prints_deployment_object.get_job_logs())