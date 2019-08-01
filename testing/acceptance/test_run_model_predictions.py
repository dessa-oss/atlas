"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import acceptance.fixtures.train_model_package as train_model_package
from acceptance.mixins.model_serving_configurator import ModelServingConfigurator

@skip('completely deprecated - to be removed along with implementation')
class TestRunModelPredictions(ModelServingConfigurator):

    @set_up
    def set_up(self):
        import subprocess

        self.set_up_model_server_config()
        model = train_model_package.validation_predictions.run()
        model.wait_for_deployment_to_complete()
        model_id = model.job_name()
        try:
            subprocess.run(['python', '-m', 'foundations', 'serving', 'deploy', 'rest', '--domain=localhost:5000', '--model-id={}'.format(model_id), '--slug=snail'], check=True)
        except subprocess.CalledProcessError as ex:
            self._tear_down()
            self.fail(str(ex))

    @tear_down
    def tear_down(self):
        self._tear_down()

    def _tear_down(self):
        import subprocess

        subprocess.run(['python', '-m', 'foundations', 'serving', 'stop'])
        self.tear_down_model_server_config()

    @let
    def input_data(self):
        return {
            'rows': [[0, 20, 100]],
            'schema': [{'name': 'Sex', 'type': 'int'}, {'name': 'Cabin', 'type': 'int'}, {'name': 'Fare', 'type': 'int'}]
        }

    def test_run_model_predictions(self):
        import requests

        response = requests.post('http://localhost:5000/v1/snail/predictions/', json=self.input_data)
        self.assertEqual(200, response.status_code)
        expected_predictions = {'rows': [[0]], 'schema': [{'name': 'Survived', 'type': 'int64'}]}
        self.assertEqual(expected_predictions, response.json())
