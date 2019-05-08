"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *
import integration.fixtures.train_model_package as train_model_package
import foundations

class TestDeployModelPackageProcess(Spec):

    @let
    def input_data(self):
        import pandas
        return pandas.DataFrame({
            "Sex": [0],
            "Cabin": [101],
            "Fare": [10]
        })

    @set_up
    def set_up(self):
        foundations.set_environment('local')

        model_package_1 = train_model_package.validation_predictions.run()
        model_package_1.wait_for_deployment_to_complete()
        self.model_package_2_id = model_package_1.job_name()
    
        model_package_2 = train_model_package.validation_predictions.run()
        model_package_2.wait_for_deployment_to_complete()
        self.model_package_2_id = model_package_2.job_name()

    @skip('not implemented')
    def test_can_load_and_predict_on_multiple_model_packages(self):
        from foundations_production.serving.package_pool import PackagePool
        
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_package_1_id)
        package_pool.add_package(self.model_package_2_id)

        prediction_1 = package_pool.run_prediction_on_package(self.model_package_1_id, self.input_data)
        prediction_2 = package_pool.run_prediction_on_package(self.model_package_2_id, self.input_data)

        expected_prediction = pandas.DataFrame({'Survived': [1]})

        self.assertEqual(expected_prediction, prediction_1)
        self.assertEqual(expected_prediction, prediction_2)


