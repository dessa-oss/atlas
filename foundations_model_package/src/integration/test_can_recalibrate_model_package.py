"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import os
import subprocess
from foundations_spec import *
import foundations
from integration.mixins.deploy_model_mixin import DeployModelMixin

@skip('not implemented')
class TestCanRecalibrateModelPackage(Spec, DeployModelMixin):

    @let
    def model_name(self):
        return self.faker.word().lower()

    @let
    def recalibrated_model_name(self):
        return self.faker.word().lower()
    @let
    def project_name(self):
        return self.faker.word().lower()

    @let
    def job_id(self):
        if self.deployment:
            return self.deployment.job_name()

    @staticmethod
    def _is_running_on_jenkins():
        return os.environ.get('RUNNING_ON_CI', 'FALSE') == 'TRUE'

    # @set_up_class
    # def set_up_class(klass):
    #     if not klass._is_running_on_jenkins():
    #         return_code = subprocess.call(['bash', '-c', './build.sh'])

    #         if return_code != 0:
    #             raise AssertionError('docker build for model package failed :(')

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import config_manager
        self._set_up_environment()

    @tear_down
    def tear_down(self):
        self._tear_down_environment(self.project_name, models=[self.model_name, self.recalibrated_model_name])

    def test_can_recalibrate_and_redeploy_server(self):
        import time
        try:
            self._set_up_in_test('model-server-with-recalibrate')
            
            # similar to orbit (serve)
            predict_result = self._try_post_to_predict_endpoint()
            self.assertEqual({'a': 21, 'b': 32}, predict_result)

            # send post request to perform the recalibrate operatoin
            recalibrate_response = self._try_post_to_recalibrate_endpoint()

            import pprint
            pprint.pprint(recalibrate_response)

            recalibrate_job_id = recalibrate_response['job_id']
            self.job_id = recalibrate_job_id
            self._wait_for_job_to_complete(recalibrate_job_id)
            
            # attempting to replace default model by ensuring only one model package exists 
            # self._tear_down_model_package(self.project_name, self.model_name, self.job_id)
            # self._tear_down_proxy()
            # self._spin_up_model_package_and_proxy(self.project_name, self.recalibrated_model_name)

            # new_predict_result = self._try_post_to_predict_endpoint()

            # print(new_predict_result) # Temporary for now

            # self.assertEqual('1', self.redis_connection.get(f'models:{self.job_id}:served').decode())
            # self.assertEqual({'a': 20 + 24 * 3600 - 60}, new_predict_result)
        except KeyboardInterrupt:
            self.fail('Interrupted by user')

    def _try_post_to_predict_endpoint(self):
        return self._try_post('predict', {'a': 20, 'b': 30})

    def _try_post_to_recalibrate_endpoint(self):
        return self._try_post('recalibrate', {'model-name': self.recalibrated_model_name, 'start_date': '2017-07-29T00:01:00', 'end_date': '2017-07-30T00:00:00'})

    def _try_post(self, endpoint, dict_payload):
        import requests

        try:
            return requests.post(f'http://localhost:{self.port}/{endpoint}', json=dict_payload).json()
        except:
            return None