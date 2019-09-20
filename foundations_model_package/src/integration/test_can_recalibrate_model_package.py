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

@skip('Not Implemented')
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
        from foundations_scheduler_core.kubernetes_api_wrapper import KubernetesApiWrapper

        self._set_up_environment()
        self._core_api = KubernetesApiWrapper().core_api()

    # @tear_down
    # def tear_down(self):
    #     self._tear_down_environment(self.project_name, models=[self.model_name, self.recalibrated_model_name])

    def test_can_recalibrate_and_redeploy_server(self):
        import time
        try:
            self._set_up_in_test('model-server-with-recalibrate')
            
            # similar to orbit (serve)
            predict_result = self._try_post_to_predict_endpoint()
            self.assertEqual({'a': 21, 'b': 32}, predict_result)

            # send post request to perform the recalibrate operatoin
            recalibrate_response = self._try_post_to_recalibrate_endpoint()
            self.assertIsNotNone(recalibrate_response)

            self.job_id = recalibrate_response['job_id']
            self._wait_for_job_to_complete(self.job_id)

            new_predict_result = self._try_post_to_predict_endpoint()

            # print(new_predict_result) # Temporary for now

            self.assertEqual('1', self.redis_connection.get(f'models:{self.job_id}:served').decode())
            self.assertEqual({'a': 20 + 24 * 3600 - 60}, new_predict_result)
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
        except Exception as e:
            print(e)
            return None

    def _wait_for_statuses(self, job_id, statuses, error_message):
        import time

        time_elapsed = 0
        timeout = 60

        while self._job_status(job_id) in statuses:
            if time_elapsed >= timeout:
                raise AssertionError(error_message)

            time_elapsed += 5
            time.sleep(5)

    def _job_status(self, job_id):
        from foundations_scheduler.pod_fetcher import get_latest_for_job

        pod = get_latest_for_job(self._core_api, job_id)

        if pod is None:
            return 'Pending'
        else:
            return pod.status.phase

    def _wait_for_job_to_complete(self, job_id):
        self._wait_for_statuses(job_id, ['Pending', 'Running'], 'job did not finish')