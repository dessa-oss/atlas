"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from acceptance.mixins.model_serving_config_mixin import ModelServingConfigMixin
import acceptance.fixtures.train_model_package as train_model_package


class TestDeployModelPackage(ModelServingConfigMixin):
    @let
    def job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        import subprocess

        self.set_up_model_server_config()
        job = train_model_package.validation_predictions.run()
        job.wait_for_deployment_to_complete()
        job_id = job.job_name()
        try:
            subprocess.run(['python', '-m', 'foundations', 'serving', 'deploy', 'rest', '--domain=localhost:5000', '--model-id={}'.format(job_id), '--slug=snail'], check=True)
        except subprocess.CalledProcessError as ex:
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