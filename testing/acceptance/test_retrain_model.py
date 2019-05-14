"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

import acceptance.fixtures.train_model_package as train_model_package

class TestRetrainModel(Spec):
    
    @let
    def features_file_name(self):
        return '/tmp/{}.pkl'.format(self.faker.uuid4())

    @let
    def targets_file_name(self):
        return '/tmp/{}.pkl'.format(self.faker.uuid4())

    @let
    def model_server_config_path(self):
        return 'model_server.config.yaml'

    @set_up
    def set_up(self):
        import os
        import subprocess

        os.environ['MODEL_SERVER_CONFIG_PATH'] = self.model_server_config_path

        job = train_model_package.validation_predictions.run()
        job.wait_for_deployment_to_complete()
        job_id = job.job_name()

        self._create_retraining_data_sets()
        self._create_model_server_config_file()

        subprocess.run(['foundations', 'serving', 'deploy', 'rest', '--domain=localhost:5000', '--model-id={}'.format(job_id), '--slug=snail'])

    @tear_down
    def tear_down(self):
        import os
        import subprocess

        subprocess.run(['foundations', 'serving', 'stop'])
        os.remove(self.features_file_name)
        os.remove(self.targets_file_name)
        os.remove(self.model_server_config_path)

    def test_retrain_creates_new_model_package(self):
        import pandas
        from pandas.testing import assert_frame_equal

        import requests

        route_url = 'http://localhost:5000/v1/snail/model/'
        payload = {
            'targets_file': 'local://{}'.format(self.targets_file_name),
            'features_file': 'local://{}'.format(self.features_file_name)
        }

        response = requests.put(route_url, json=payload)
        self.assertEqual(202, response.status_code)

        new_model_package_id = response.json()['created_job_uuid']

        new_model_package = self._get_model_package(new_model_package_id, 30)

        production_dataset = pandas.DataFrame({
            'Sex': [0, 3],
            'Cabin': [101, 4],
            'Fare': [20, 10]
        })

        preprocessed_production_dataset = new_model_package.preprocessor(production_dataset)
        production_predictions = new_model_package.model.predict(preprocessed_production_dataset)

        expected_predictions = pandas.DataFrame({
            'Survived': [0, 1]
        })

        actual_predictions = production_predictions.run_same_process()
        assert_frame_equal(expected_predictions, actual_predictions)

    def _get_model_package(self, model_package_id, timeout):
        import time
        from foundations_production import load_model_package

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                return load_model_package(model_package_id)
            except FileNotFoundError:
                time.sleep(3)

        raise AssertionError('model package {} not found after {} seconds'.format(model_package_id, timeout))

    def _create_retraining_data_sets(self):
        import pandas

        features = pandas.DataFrame({
            'Sex': [1, 5],
            'Cabin': [1, 0],
            'Fare': [15, -100],
        })

        targets = pandas.DataFrame({
            'Survived': [0, 1]
        })

        self._save_dataframe(features, self.features_file_name)
        self._save_dataframe(targets, self.targets_file_name)
        
    def _save_dataframe(self, dataframe, file_name):
        import pickle

        with open(file_name, 'wb') as dataframe_file:
            pickle.dump(dataframe, dataframe_file)

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