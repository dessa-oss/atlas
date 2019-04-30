"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import foundations
import foundations_production
import acceptance.fixtures.train_model_package as train_model_package
import acceptance.fixtures.production_model_package as production_model_package
import pandas

class TestModelPackage(Spec):

    def test_can_create_and_consume_model_package(self):
        job = train_model_package.validation_predictions.run()
        job.wait_for_deployment_to_complete()
        job_id = job.job_name()

        model_package = foundations_production.load_model_package(job_id)

        production_dataset = pandas.DataFrame({
            "Sex": [0],
            "Cabin": [101],
            "Fare": [10]
        })
        preprocessed_production_dataset = model_package.preprocessor(production_dataset)
        production_predictions = model_package.model(preprocessed_production_dataset, preprocessed_production_dataset)

        production_job = foundations.create_stage(production_model_package.log_predictions_for_assertion)(production_predictions).run()
        production_job.wait_for_deployment_to_complete()

        metrics = foundations.get_metrics_for_all_jobs('default')
        production_predictions = metrics.loc[metrics['job_id'] == production_job.job_name()].iloc[0]['predictions']

        self.assertEqual(1, production_predictions)