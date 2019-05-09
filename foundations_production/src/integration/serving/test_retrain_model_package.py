"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from integration.fixtures.train_model_package import validation_predictions

class TestRetrainModelPackage(Spec):
    @let
    def features_file_name(self):
        return '/tmp/{}.pkl'.format(self.faker.uuid4())

    @let
    def targets_file_name(self):
        return '/tmp/{}.pkl'.format(self.faker.uuid4())

    @set_up
    def set_up(self):
        job = validation_predictions.run()
        job.wait_for_deployment_to_complete()
        self._job_id = job.job_name()

        self._create_retraining_data_sets()

    @tear_down
    def tear_down(self):
        import os

        os.remove(self.features_file_name)
        os.remove(self.targets_file_name)

    @skip('not ready yet')
    def test_retrain_runs_retraining_foundations_job(self):
        import pandas
        from pandas.testing import assert_frame_equal

        from foundations_production import load_model_package
        from foundations_production.serving import create_retraining_job

        features_location = 'local://{}'.format(self.features_file_name)
        targets_location = 'local://{}'.format(self.targets_file_name)

        retraining_job = create_retraining_job(self._job_id, features_location=features_location, targets_location=targets_location).run()
        retraining_job.wait_for_deployment_to_complete()
        new_model_package_id = retraining_job.job_name()

        new_model_package = load_model_package(new_model_id)

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