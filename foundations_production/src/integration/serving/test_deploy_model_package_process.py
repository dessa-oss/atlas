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
        return {
            'rows': [[0, 20, 100]], 
            'schema': [{'name': 'Sex', 'type': 'int'}, {'name': 'Cabin', 'type': 'int'}, {'name': 'Fare', 'type': 'int'}]
        }
    
    @let
    def predictions(self):
        return {
            'rows': [[0]],
            'schema': [{'name': 'Survived', 'type': 'int64'}]
        }

    @set_up
    def set_up(self):
        from integration.config import integration_job_name

        model_package_1 = train_model_package.validation_predictions.run_same_process()
        self.model_package_1_id = integration_job_name

    def test_can_load_and_predict_on_a_model_packages(self):
        from foundations_production.serving.package_pool import PackagePool
        
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_package_1_id)

        communicator_to_package = package_pool.get_communicator(self.model_package_1_id)
        communicator_to_package.set_action_request(self.input_data)
        predictions = communicator_to_package.get_response()

        self.assertEqual(self.predictions, predictions)


