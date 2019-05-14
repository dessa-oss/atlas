"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *
import integration.fixtures.train_model_package as titanic_model_package
import integration.fixtures.fake_model_package as fake_model_package

class TestDeployModelPackageProcess(Spec):

    @let
    def titanic_input_data(self):
        return {
            'rows': [[0, 20, 100]], 
            'schema': [{'name': 'Sex', 'type': 'int'}, {'name': 'Cabin', 'type': 'int'}, {'name': 'Fare', 'type': 'int'}]
        }
    
    @let
    def titanic_predictions(self):
        return {
            'rows': [[0]],
            'schema': [{'name': 'Survived', 'type': 'int64'}]
        }
    
    @let
    def fake_input_data(self):
        return {
            'rows': [['value', 43234], ['spider', 323]], 
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }
    @let
    def model_id(self):
        return self.faker.uuid4()

    @let
    def fake_predictions(self):
        return {
            'rows': [['value transformed predicted', 43667], ['spider transformed predicted', 756]], 
            'schema': [{'name': '1st column', 'type': 'object'}, {'name': '2nd column', 'type': 'int64'}]
        }

    @set_up_class
    def set_up(self):
        model_package = titanic_model_package.validation_predictions.run()
        model_package.wait_for_deployment_to_complete()
        self.titanic_model_package_id = model_package.job_name()
    
    def test_exception_raised_when_model_package_does_not_exist(self):
        from foundations_production.serving.package_pool import PackagePool
        
        package_pool = PackagePool(active_package_limit=1)
        with self.assertRaises(KeyError) as context:
            package_pool.add_package(self.model_id)

        self.assertTrue('Model Package ID {} does not exist'.format(self.model_id) in str(context.exception))

    def test_can_load_and_predict_on_a_model_package(self):
        from foundations_production.serving.package_pool import PackagePool
        
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.titanic_model_package_id)
        predictions = self._get_titanic_predictions(package_pool)

        self.assertEqual(self.titanic_predictions, predictions)

    def test_can_load_and_predict_on_multiple_model_packages(self):
        from foundations_production.serving.package_pool import PackagePool

        self._run_fake_model_package()
        
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.titanic_model_package_id)
        package_pool.add_package(self.fake_model_package_id)

        actual_titanic_predictions = self._get_titanic_predictions(package_pool)
        actual_fake_predictions = self._get_fake_model_package_predictions(package_pool)

        self.assertEqual(self.titanic_predictions, actual_titanic_predictions)
        self.assertEqual(self.fake_predictions, actual_fake_predictions)
    
    def _run_fake_model_package(self):        
        model_package = fake_model_package.validation_predictions.run()
        model_package.wait_for_deployment_to_complete()
        self.fake_model_package_id = model_package.job_name()
    
    def _get_titanic_predictions(self, package_pool):
        communicator_to_package = package_pool.get_communicator(self.titanic_model_package_id)
        communicator_to_package.set_action_request(self.titanic_input_data)
        return communicator_to_package.get_response()
    
    def _get_fake_model_package_predictions(self, package_pool):
        communicator_to_fake_package = package_pool.get_communicator(self.fake_model_package_id)
        communicator_to_fake_package.set_action_request(self.fake_input_data)
        return communicator_to_fake_package.get_response()