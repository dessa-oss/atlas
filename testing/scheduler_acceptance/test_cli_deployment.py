"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestCliDeployment(Spec):
    
    @let
    def cli_config(self):
        from foundations_spec.extensions import get_network_address
        docker_address = get_network_address('docker0')
        return {
            'job_deployment_env': 'scheduler_plugin',
            'results_config': {
                'archive_end_point': '/archive',
                'redis_end_point': 'redis://{}:6379'.format(docker_address)
            },
            'cache_config': {
                'end_point': '/cache'
            },
            'ssh_config': {
                'user': 'job-uploader',
                'host': 'localhost',
                'code_path': '/jobs',
                'result_path': '/jobs',
                'key_path': '~/.ssh/id_foundations_scheduler',
                'port': 31222
            },
            'log_level': 'INFO',
            'obfuscate_foundations': False
        }

    @let
    def yaml_cli_config(self):
        import yaml
        return yaml.dump(self.cli_config)
    
    @set_up
    def set_up(self):
        import shutil
        import os
        import os.path

        shutil.rmtree("test-cli-init", ignore_errors=True)
        if os.path.isfile('~/.foundations/job_data/projects/my-foundations-project.tracker'):
            os.remove('~/.foundations/job_data/projects/my-foundations-project.tracker')

    def test_cli_can_deploy_job_created_by_init(self):
        import subprocess

        subprocess.call(["python", "-m", "foundations", "init", "test-cli-init"])

        with open('test-cli-init/config/scheduler.config.yaml', 'w+') as file:
            file.write(self.yaml_cli_config)

        driver_deploy_result = subprocess.run(["/bin/bash", "-c", "cd test-cli-init && python -m foundations deploy project_code/driver.py --env scheduler"])
        self._assert_deployment_was_successful(driver_deploy_result)

    def _assert_deployment_was_successful(self, driver_deploy_result):
        if driver_deploy_result.returncode != 0:
            error_message = 'Driver deployment failed:\n{}'.format(driver_deploy_result.stderr)
            raise AssertionError(error_message)