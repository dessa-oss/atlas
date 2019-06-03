"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestGetJobLogs(Spec):

    @let
    def config_path(self):
        import os.path as path
        return path.join('config', 'local_scheduler.config.yaml')

    @let
    def fake_job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        self._create_config()

    @tear_down
    def tear_down(self):
        self._delete_config()

    def test_get_logs_for_job_that_does_not_exist_prints_error_message(self):
        import subprocess

        error_message = 'Error: Job `{}` does not exist for environment `local_scheduler`'.format(self.fake_job_id)
        command_to_run = ['foundations', 'retrieve', 'logs', '--job_id={}'.format(self.fake_job_id), '--env=local_scheduler']
        cli_result = subprocess.run(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cli_stdout = cli_result.stdout
        cli_stdout = cli_stdout.decode().rstrip('\n') 

        self.assertEqual(1, cli_result.returncode)
        self.assertEqual(error_message, cli_stdout)

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
            'obfuscate_foundations': False
        }

        with open(self.config_path, 'w') as config_file:
            yaml.dump(config_dictionary, config_file)

    def _delete_config(self):
        import os
        os.remove(self.config_path)


    
