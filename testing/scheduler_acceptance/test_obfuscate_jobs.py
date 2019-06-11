"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_spec.helpers import set_up, tear_down
from foundations_spec import *
from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
from foundations import config_manager
from foundations_ssh.sftp_bucket import SFTPBucket
from foundations import log_metric

class TestObfuscateJobs(Spec):

    @tear_down
    def tear_down(self):
        from scheduler_acceptance.cleanup import cleanup
        config_manager['obfuscate_foundations'] = False
        cleanup()
        self._delete_config()

    @let
    def config_path(self):
        import os.path as path
        return path.join('config', 'local_scheduler.config.yaml')
    
    @set_up
    def set_up(self):
        self._create_config()

        
    def test_job_obfuscates_source_code_when_remote_and_obfuscate_true(self):
        import foundations
        import time 
        from scheduler_acceptance.fixtures.stages import add_two_numbers, read_init_file
        
        config_manager['obfuscate_foundations'] = True

        read_init_file = foundations.create_stage(read_init_file)
        read_init_file_stage = read_init_file()

        log_metric = foundations.create_stage(self._log_a_metric)
        log_metric_stage = log_metric(read_init_file_stage)

        job = log_metric_stage.run()
        job.wait_for_deployment_to_complete()
        time.sleep(3)

        metrics = foundations.get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == job.job_name()]

        self.assertTrue(self._check_source_code_obfuscated(job_metrics))
    
    def test_job_does_not_obfuscates_source_code_when_remote_and_obfuscate_false(self):
        import foundations
        import time
        from scheduler_acceptance.fixtures.stages import add_two_numbers, read_init_file
        
        config_manager['obfuscate_foundations'] = False

        read_init_file = foundations.create_stage(read_init_file)
        read_init_file_stage = read_init_file()

        log_metric = foundations.create_stage(self._log_a_metric)
        log_metric_stage = log_metric(read_init_file_stage)

        job = log_metric_stage.run()
        job.wait_for_deployment_to_complete()
        time.sleep(3)

        metrics = foundations.get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == job.job_name()]

        self.assertFalse(self._check_source_code_obfuscated(job_metrics))


    def test_job_still_completes_when_obfuscated(self):
        import foundations
        import time
        from scheduler_acceptance.fixtures.stages import add_two_numbers

        config_manager['obfuscate_foundations'] = True

        add_two_numbers = foundations.create_stage(add_two_numbers)
        add_two_numbers_deployment_object = add_two_numbers(3, 5).run()
        add_two_numbers_deployment_object.wait_for_deployment_to_complete()
        time.sleep(10)

        self.assertEqual(add_two_numbers_deployment_object.get_job_status(), 'completed')
    

    def _check_source_code_obfuscated(self, job_metrics):
        return job_metrics['init_file'].iloc[0] == '__pyarmor__'
    
    def _create_config(self):
        from foundations import config_manager
        import yaml

        config_dictionary = {
            'results_config': {
                'archive_end_point': '/archive', 
                'redis_end_point': config_manager['redis_url']
            },
            'ssh_config': {
                'code_path': '/jobs',
                'host': config_manager['remote_host'],
                'key_path': '~/.ssh/id_foundations_scheduler',
                'port': 31222,
                'result_path': '/jobs',
                'user': 'job-uploader'
            },
            'cache_config': {'end_point': '/cache'},
            'job_deployment_env': 'scheduler_plugin',
            'obfuscate_foundations': False,
            'log_level': 'DEBUG'
        }

        with open(self.config_path, 'w') as config_file:
            yaml.dump(config_dictionary, config_file)
    
    def _delete_config(self):
        import os
        os.remove(self.config_path)

    @staticmethod
    def _log_a_metric(value):
        log_metric('init_file', value)