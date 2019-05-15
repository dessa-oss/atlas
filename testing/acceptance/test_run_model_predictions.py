"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import acceptance.fixtures.train_model_package as train_model_package


class TestRunModelPredictions(Spec):

    @set_up
    def set_up(self):
        import subprocess

        model = train_model_package.validation_predictions.run()
        model.wait_for_deployment_to_complete()
        model_id = model.job_name()
        
        subprocess.run(['python', '-m', 'foundations', 'serving', 'deploy', 'rest', '--domain=localhost:5000', '--model-id={}'.format(model_id), '--slug=snail'])

    @let
    def input_data(self):
        import pandas
        return pandas.DataFrame({
            "Sex": [0],
            "Cabin": [101],
            "Fare": [10]
        })

    @skip('not yet implemented')
    def test_run_model_predictions(self):
        import requests
        import pandas

        response = requests.post('https://ip/v1/snail/predictions', json=self.input_data.to_json())
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json['prediction_id'])

        get_response = requests.get('https://ip/v1/snail/predictions/1')
        self.assertEqual(200, get_response.status_code)

        expected_prediction = pandas.DataFrame({'predictions': [1]})
        self.assertEqual(expected_prediction.to_json(), get_response.json)