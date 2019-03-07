"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_internal.testing.helpers import set_up, tear_down
from foundations_internal.testing.helpers.spec import Spec
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
        import foundations

        from remote_acceptance.prototype.fixtures.stages import function_that_prints

        function_that_prints = foundations.create_stage(function_that_prints)
        function_that_prints_deployment_object = function_that_prints().run()

        self.assertIn(function_that_prints_deployment_object.get_jobs(), "I am a function \n I print things")