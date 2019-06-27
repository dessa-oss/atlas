"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from acceptance.mixins.model_serving_configurator import ModelServingConfigurator
from acceptance.mixins.model_package_deployer import ModelPackageDeployer


class TestDeployModelPackage(ModelServingConfigurator, ModelPackageDeployer):
    @let
    def job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        import subprocess

        self.set_up_model_server_config()
        job_id = self.deploy_model_package()
        try:
            model_server_deploy_command = ['python', '-m', 'foundations', 'serving', 'deploy', 'rest', '--domain=localhost:5000', '--model-id={}'.format(job_id), '--slug=snail']
            completed_process = subprocess.run(model_server_deploy_command, check=True, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as ex:
            print(completed_process.stderr)
            subprocess.run(['python', '-m', 'foundations', 'serving', 'stop'])
            self.fail(str(ex))

    @tear_down
    def tear_down(self):
        import subprocess

        subprocess.run(['python', '-m', 'foundations', 'serving', 'stop'])
        self.tear_down_model_server_config()

    def test_deploy_model_package_via_cli(self):
        base_url = 'http://localhost:5000/v1/snail'
        self._assert_successful_get(base_url)
        self._assert_successful_get(base_url + '/model')
        self._assert_successful_get(base_url + '/predictions')

    def _assert_successful_get(self, url):
        import requests

        response = requests.get(url)
        self.assertEqual(200, response.status_code)
