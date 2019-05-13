"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestDeployModelPackage(Spec):
    @let
    def job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        import subprocess

        subprocess.run(['foundations', 'serving', 'deploy', 'rest', '--domain=localhost:5000', '--model-id={}'.format(self.job_id), '--slug=snail'])

    @tear_down
    def tear_down(self):
        import subprocess

        subprocess.run(['foundations', 'serving', 'stop'])

    def test_deploy_model_package_via_cli(self):
        base_url = 'http://localhost:5000/v1/snail'
        self._assert_successful_get(base_url)
        self._assert_successful_get(base_url + '/model')
        self._assert_successful_get(base_url + '/predictions')

    def _assert_successful_get(self, url):
        import requests

        response = requests.get(url)
        self.assertEqual(200, response.status_code)