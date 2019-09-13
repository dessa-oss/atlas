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

@skip('fails on jenkins')
class TestCanDeployModelServer(Spec, DeployModelMixin):

    @let
    def model_name(self):
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

    @set_up_class
    def set_up_class(klass):
        if not klass._is_running_on_jenkins():
            return_code = subprocess.call(['bash', '-c', './build.sh'])

            if return_code != 0:
                raise AssertionError('docker build for model package failed :(')

    @set_up
    def set_up(self):
        self._set_up_environment()

    @tear_down
    def tear_down(self):
        self._tear_down_environment(self.project_name, models=[self.model_name])

    def test_can_deploy_server(self):
        try:
            self._set_up_in_test('model-server')

            result = self._try_post_to_root_endpoint()
            predict_result = self._try_post_to_predict_endpoint()

            self.assertEqual({'a': 2, 'b': 4}, result)
            self.assertEqual({'a': 21, 'b': 32}, predict_result)

            self.assertEqual('1', self.redis_connection.get(f'models:{self.job_id}:served').decode())
        except KeyboardInterrupt:
            self.fail('Interrupted by user')

    def test_can_hit_evaluate_endpoint(self):
        import time
        import pickle
        try:
            self._set_up_in_test('model-server-with-evaluate')

            self._try_post_to_evaluate_endpoint('october')
            time.sleep(self.sleep_time)
            self._try_post_to_evaluate_endpoint('january')
            time.sleep(self.sleep_time)

            production_metrics_from_redis = self.redis_connection.hgetall(f'projects:{self.project_name}:models:{self.model_name}:production_metrics')
            production_metrics = {metric_name.decode(): pickle.loads(serialized_metrics) for metric_name, serialized_metrics in production_metrics_from_redis.items()}
            production_metrics['MSE'].sort(key=lambda entry: entry[0])

            expected_production_metrics = {
                'roc_auc': [('october', 66), ('january', 66)],
                'MSE': [('january', 1), ('january_again', 2), ('october', 1), ('october_again', 2)]
            }

            self.assertEqual(expected_production_metrics, production_metrics)
        except KeyboardInterrupt:
            self.fail('Interrupted by user')

    def _try_post_to_root_endpoint(self):
        return self._try_post('', {'a': 1, 'b': 2})

    def _try_post_to_predict_endpoint(self):
        return self._try_post('predict', {'a': 20, 'b': 30})

    def _try_post_to_evaluate_endpoint(self, eval_period):
        response = self._try_post('evaluate', {'eval_period': eval_period})

        if response is None:
            self.fail('post to evaluate failed :(')

    def _try_post(self, endpoint, dict_payload):
        import requests

        try:
            return requests.post(f'http://localhost:{self.port}/{endpoint}', json=dict_payload).json()
        except:
            return None