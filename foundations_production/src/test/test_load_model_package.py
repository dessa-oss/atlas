"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *
from foundations_production import load_model_package

class TestLoadModelPackage(Spec):

    mock_pipeline_archiver = let_mock()
    mock_preprocessor = let_mock()
    
    @let_now
    def mock_load_preprocessor(self):
        mock_load_preprocessor = self.patch('foundations_production.preprocessor_class.Preprocessor.load_preprocessor',ConditionalReturn())
        mock_load_preprocessor.return_when(self.mock_preprocessor, self.mock_pipeline_archiver, 'transformer', self.job_id)
        return mock_load_preprocessor

    @let
    def job_id(self):
        return self.faker.uuid4() 

    @let_now
    def mock_get_pipeline_archiver(self):
        mock_get_pipeline_archiver = self.patch('foundations_contrib.archiving.get_pipeline_archiver_for_job', ConditionalReturn())
        mock_get_pipeline_archiver.return_when(self.mock_pipeline_archiver, self.job_id)
        return mock_get_pipeline_archiver
    
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
    
    def test_load_model_package_returns_correct_preprocessor(self):
        model_package = load_model_package(self.job_id)
        self.assertEqual(self.mock_preprocessor, model_package.preprocessor)
