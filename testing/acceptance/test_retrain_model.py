"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

import acceptance.fixtures.train_model_package as train_model_package

@skip
class TestRetrainModel(Spec):
    
    @let
    def features_file_name(self):
        return '/tmp/{}.pkl'.format(self.faker.uuid4())

    @let
    def targets_file_name(self):
        return '/tmp/{}.pkl'.format(self.faker.uuid4())

    @set_up
    def set_up(self):
        import subprocess
        job = train_model_package.validation_predictions.run()
        job.wait_for_deployment_to_complete()
        job_id = job.job_name()

        self._create_retraining_data_sets()

        subprocess.run(['foundations', 'serving', 'deploy', 'rest', '--domain=localhost:5000', '--model-id={}'.format(job_id), '--slug=snail'])

    @tear_down
    def tear_down(self):
        import os
        import subprocess

        subprocess.run(['foundations', 'serving', 'stop'])
        os.remove(self.features_file_name)
        os.remove(self.targets_file_name)

    def test_retrain_creates_new_model_package(self):
        import requests

        route_url = 'http://localhost:5000/v1/snail/model'
        payload = {
            'targets_file': 'local://{}'.format(self.targets_file_name),
            'features_file': 'local://{}'.format(self.features_file_name)
        }

        response = requests.put(route_url, json=payload)
        self.assertEqual(202, response.status_code)

        new_model_package_id = response.json()['created_job_uuid']

        self._assert_model_package_exists(new_model_package_id, 30)

    def _assert_model_package_exists(self, model_package_id, timeout):
        import time
        from foundations_production import load_model_package

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                load_model_package(model_package_id)
                return
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