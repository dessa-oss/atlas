"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *
from foundations_production import load_model_package

class TestLoadModelPackage(Spec):

    mock_transformer_callback = let_mock()
    mock_pipeline_archiver = let_mock()
    mock_production_data = let_mock()

    @let
    def job_id(self):
        return self.faker.uuid4() 
    
    @let_now
    def mock_get_pipeline_archiver(self):
        mock_get_pipeline_archiver = self.patch('foundations_contrib.archiving.get_pipeline_archiver_for_job', ConditionalReturn())
        mock_get_pipeline_archiver.return_when(self.mock_pipeline_archiver, self.job_id)
        return mock_get_pipeline_archiver

    @set_up
    def set_up(self):
        self.mock_pipeline_archiver.fetch_artifact = ConditionalReturn()
        self.mock_pipeline_archiver.fetch_artifact.return_when(self.mock_transformer_callback, 'preprocessor/transformer.pkl')

    def test_load_model_package_loads_transformer_preprocessor(self):
        model_package = load_model_package(self.job_id)
        model_package.preprocessor(self.mock_production_data)
        self.mock_transformer_callback.assert_called_with(self.mock_production_data)

    def test_load_model_package_loads_transformer_preprocessor_with_correct_name(self):
        model_package = load_model_package(self.job_id)
        model_package.preprocessor(self.mock_production_data)
        new_transformer_index = model_package.preprocessor.new_transformer(None)
        self.assertEqual('transformer_0', new_transformer_index)

    def test_load_model_package_loads_transformer_preprocessor_with_job_id(self):
        model_package = load_model_package(self.job_id)
        model_package.preprocessor(self.mock_production_data)
        self.assertEqual(self.job_id, model_package.preprocessor.job_id.run_same_process())

    def test_load_model_package_loads_model_preprocessor_with_correct_name(self):
        model_package = load_model_package(self.job_id)
        new_transformer_index = model_package.model.new_transformer(None)
        self.assertEqual('model_0', new_transformer_index)

    def test_load_model_package_loads_model_preprocessor_with_job_id(self):
        model_package = load_model_package(self.job_id)
        self.assertEqual(self.job_id, model_package.model.job_id)

    def test_model_preprocessor_is_production_model(self):
        from foundations_production.production_model import ProductionModel

        model_package = load_model_package(self.job_id)
        self.assertIsInstance(model_package.model, ProductionModel)   
    
    def test_transformer_preprocessor_inference_mode_is_true(self):
        model_package = load_model_package(self.job_id)
        self.assertTrue(model_package.preprocessor.get_inference_mode())
