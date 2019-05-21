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
    mock_is_job_completed = let_patch_mock('foundations_contrib.job_data_redis.JobDataRedis.is_job_completed')
    
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

    @set_up
    def set_up(self):
        self.mock_is_job_completed.return_value = True

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

    def test_load_model_package_raises_error_if_job_not_completed(self):
        from foundations_production.exceptions import MissingModelPackageException

        self.mock_is_job_completed.return_value = False
        with self.assertRaises(MissingModelPackageException) as context:
            load_model_package(self.job_id)
        
        self.assertEqual(self.job_id, str(context.exception))

    def test_load_model_package_calls_is_job_completed_with_correct_arguments(self):
        from foundations_contrib.global_state import redis_connection
        load_model_package(self.job_id)
        self.mock_is_job_completed.assert_called_with(self.job_id, redis_connection)
