"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_internal.testing.helpers import set_up, tear_down
from foundations_internal.testing.helpers.spec import Spec


class TestObfuscateJobs(Spec):

    @tear_down
    def tear_down(self):
        from remote_acceptance.cleanup import cleanup
        cleanup()
    
    @set_up
    def set_up(self):
        from foundations import config_manager
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment


        import remote_acceptance.config.remote_config as remote_config

        remote_config.config()

        config_manager['obfuscate_foundations'] = True

        config_manager['deployment_implementation'] = {
            'deployment_type': SFTPJobDeployment
        }



    def test_job_still_completes_when_obfuscated(self):
        import foundations
        import time

        from remote_acceptance.fixtures.stages import add_two_numbers

        add_two_numbers = foundations.create_stage(add_two_numbers)
        add_two_numbers_deployment_object = add_two_numbers(3, 5).run()
        add_two_numbers_deployment_object.wait_for_deployment_to_complete()
        time.sleep(3)

        self.assertEqual(add_two_numbers_deployment_object.get_job_status(), 'Completed')
