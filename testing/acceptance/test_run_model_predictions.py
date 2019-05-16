"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import acceptance.fixtures.train_model_package as train_model_package


class TestRunModelPredictions(Spec):

    @let
    def model_server_config_path(self):
        return 'model_server.config.yaml'

    @set_up
    def set_up(self):
        import subprocess
        import os

        os.environ['MODEL_SERVER_CONFIG_PATH'] = self.model_server_config_path

        model = train_model_package.validation_predictions.run()
        model.wait_for_deployment_to_complete()
        model_id = model.job_name()
        self._create_model_server_config_file()

        subprocess.run(['python', '-m', 'foundations', 'serving', 'deploy', 'rest', '--domain=localhost:5000', '--model-id={}'.format(model_id), '--slug=snail'])

    @tear_down
    def tear_down(self):
        import os
        import subprocess

        subprocess.run(['python', '-m', 'foundations', 'serving', 'stop'])
        os.remove(self.model_server_config_path)

    @let
    def input_data(self):
        return {
            'rows': [[0, 20, 100]], 
            'schema': [{'name': 'Sex', 'type': 'int'}, {'name': 'Cabin', 'type': 'int'}, {'name': 'Fare', 'type': 'int'}]
        }

    def test_run_model_predictions(self):
        import requests

        response = requests.post('http://localhost:5000/v1/snail/predictions', json=self.input_data)
        self.assertEqual(200, response.status_code)
        expected_predictions = {'rows': [[0]], 'schema': [{'name': 'Survived', 'type': 'int64'}]}
        self.assertEqual(expected_predictions, response.json())
    

    def _create_model_server_config_file(self):
        from acceptance.config import ARCHIVE_ROOT
        import yaml
        import os.path as path

        config_dictionary = {
            'job_deployment_env': 'local',
            'results_config': {
                'archive_end_point': 'local://' + path.dirname(ARCHIVE_ROOT)
            },
            'cache_config': {},
            'obfuscate_foundations': False
        }

        with open(self.model_server_config_path, 'w') as config_file:
            yaml.dump(config_dictionary, config_file)