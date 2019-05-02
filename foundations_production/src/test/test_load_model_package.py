"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *
from foundations_production import load_model_package
class MockClass(object):
    def __call__(self, *args):
        return args[0]

class TestLoadModelPackage(Spec):

    mock_transformer_callback = let_mock()
    mock_pipeline_archiver = let_mock()
    mock_production_data = let_mock()

    @let
    def job_id(self):
        return self.faker.uuid4() 

    @let
    def mock_class(self):
        return MockClass()
    
    @let
    def serialized_mock_class(self):
        from foundations_internal.serializer import serialize
        return serialize(self.mock_class)
    
    @let_now
    def foundations_context(self):
        from foundations_internal.foundations_context import FoundationsContext
        return self.patch('foundations_contrib.global_state.foundations_context', FoundationsContext(self.pipeline))
    
    @let_now
    def pipeline_context(self):
        from foundations_internal.pipeline_context import PipelineContext
        return PipelineContext()

    @let_now
    def pipeline(self):
        from foundations_internal.pipeline import Pipeline
        return Pipeline(self.pipeline_context)

    @set_up
    def set_up_foundations_context(self):
        self.pipeline_context.file_name = self.job_id

    
    @let
    def fake_data(self):
        return self.faker.sha1()

    @let_now
    def mock_get_pipeline_archiver(self):
        mock_get_pipeline_archiver = self.patch('foundations_contrib.archiving.get_pipeline_archiver_for_job', ConditionalReturn())
        mock_get_pipeline_archiver.return_when(self.mock_pipeline_archiver, self.job_id)
        return mock_get_pipeline_archiver

    @set_up
    def set_up(self):
        self.mock_pipeline_archiver.fetch_artifact = ConditionalReturn()
        self.mock_pipeline_archiver.fetch_artifact.return_when(self.serialized_mock_class, 'preprocessor/transformer.pkl')

    def test_load_model_package_loads_transformer_preprocessor(self):
        model_package = load_model_package(self.job_id)
        actual_value = model_package.preprocessor(self.fake_data)
        self.assertEqual(self.fake_data, actual_value.run_same_process())

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
