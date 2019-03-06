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
from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
from foundations import config_manager

class TestObfuscateJobs(Spec):

    @tear_down
    def tear_down(self):
        from remote_acceptance.cleanup import cleanup
        cleanup()
    
    @set_up
    def set_up(self):
        import remote_acceptance.config.remote_config as remote_config

        remote_config.config()

        
    def test_job_obfuscates_source_code_when_remote_and_obfuscate_true(self):
        import foundations
        import time
        from remote_acceptance.fixtures.stages import add_two_numbers
        

        config_manager['obfuscate_foundations'] = True

        config_manager['deployment_implementation'] = {
            'deployment_type': SFTPJobDeployment
        }

        add_two_numbers = foundations.create_stage(add_two_numbers)
        add_two_numbers_deployment_object = add_two_numbers(3, 5).run()
        add_two_numbers_deployment_object.wait_for_deployment_to_complete()
        time.sleep(3)

        self.assertTrue(self._check_source_code_obfuscated(add_two_numbers_deployment_object.job_name()))


    def test_job_still_completes_when_obfuscated(self):
        import foundations
        import time
        from remote_acceptance.fixtures.stages import add_two_numbers

        config_manager['obfuscate_foundations'] = True

        config_manager['deployment_implementation'] = {
            'deployment_type': SFTPJobDeployment
        }

        add_two_numbers = foundations.create_stage(add_two_numbers)
        add_two_numbers_deployment_object = add_two_numbers(3, 5).run()
        add_two_numbers_deployment_object.wait_for_deployment_to_complete()
        time.sleep(3)

        self.assertEqual(add_two_numbers_deployment_object.get_job_status(), 'Completed')
    

    def _check_source_code_obfuscated(self, job_id):
        import os
        import tarfile
        import shutil

        current_dir = os.getcwd()

        job_archive_location = '{}_archive'.format(config_manager['code_path'])
        os.chdir(job_archive_location)  

        job_tar_name = '{}.tgz'.format(job_id)

        foundations_init_file_location = os.path.join(job_id, 'foundations', '__init__.py')

        with tarfile.open(job_tar_name, "r:gz") as tar:
            tar.extract(foundations_init_file_location)
        
        with open(foundations_init_file_location, 'rb') as init_file:
            file_head = init_file.readline()[0:11]
        
        os.chdir(current_dir)
        shutil.rmtree(os.path.join(job_archive_location, job_id))
        
        return file_head == b'__pyarmor__'