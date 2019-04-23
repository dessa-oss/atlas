"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *

from integration.fixtures.stages import log_predictions_for_assertion
import foundations
import foundations_production

log_predictions_for_assertion = foundations.create_stage(log_predictions_for_assertion)

class TestPreprocessor(Spec):

    class AddAverageToValueTransformer(object):

        def __init__(self):
            self.average = 0

        def fit(self, data):
            self.average = data.mean()

        def transform(self, data):
            return data + self.average

    @skip('Not ready yet')
    def test_can_create_and_consume_preprocessor_from_model_package(self):
        foundations.set_project_name('production_titanic_test_integration')

        @foundations_production.preprocessor
        def preprocessor(input_data):
            transformer = foundations_production.Transformer(["Sex", "Cabin"], self.AddAverageToValueTransformer)
            transformer.fit(input_data)
            return transformer.transform(input_data)

        train_data = pandas.DataFrame({
            "Sex": [0, 2, 4],
            "Cabin": [200, 100, 0]
        })

        validation_data = pandas.DataFrame({
            "Sex": [0],
            "Cabin": [101]
        })

        preprocessed_train_data = preprocessor(train_data)

        preprocessor.set_inference_mode()
        preprocessed_validation_data = preprocessor(validation_data)

        job = preprocessed_validation_data.run()
        
        job.wait_for_deployment_to_complete()
        job_id = job.job_name()

        self._assert_preprocessor_results_are_as_expected([2], job_id, 'preprocessed_data_sex')
        self._assert_preprocessor_results_are_as_expected([201], job_id, 'preprocessed_data_cabin')

        production_dataset = pandas.DataFrame({
            "Sex": [0, 1],
            "Cabin": [101, 202]
        })

        model_package = foundations_production.load_model_package(job_id)

        preprocessed_production_dataset = model_package.preprocessor(production_dataset)
        production_job = log_predictions_for_assertion(production_predictions).run()

        production_job.wait_for_deployment_to_complete()

        self._assert_preprocessor_results_are_as_expected([2, 3], production_job.job_name(), 'preprocessed_data_sex')
        self._assert_preprocessor_results_are_as_expected([201, 302], production_job.job_name(), 'preprocessed_data_cabin')

    def _assert_preprocessor_results_are_as_expected(expected, job_id, metric_name):
        metrics = foundations.get_metrics_for_all_jobs('production_titanic_test_integration')
        metric_values = metrics.loc[metrics['job_id'] == job_id].iloc[0][metric_name]
        self.assertEqual(expected, metric_values)