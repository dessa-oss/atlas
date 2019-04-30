"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.production_model import ProductionModel

class TestProductionModel(Spec):

    global_preprocessor = let_patch_mock('foundations_production.preprocessor_class.Preprocessor.active_preprocessor')
    artifact_archive = let_mock()
    foundations_context = let_patch_mock('foundations_production.model_class.foundations_context')
    pipeline_archiver = let_mock()
    artifact_archive = let_mock()

    @let_now
    def job_id(self):
        job_id = self.faker.uuid4()
        self.foundations_context.job_id.return_value = job_id
        return job_id
    
    mock_base_transformer = let_mock()

    def create_base_transformer_callback(self, model, user_transformer_stage):
        self.assertIsInstance(model, ProductionModel)
        self.assertIsNone(user_transformer_stage)
        return self.mock_base_transformer

    @let_now
    def mock_base_transformer_klass(self):
        klass = self.patch('foundations_production.base_transformer.BaseTransformer')
        klass.side_effect = self.create_base_transformer_callback

        return klass

    @let
    def fake_args(self):
        return self.faker.words()

    @let
    def fake_kwargs(self):
        return self.faker.pydict()

    @let
    def model(self):
        return ProductionModel(self.job_id)

    def test_construction_calls_fit(self):
        self.model
        self.mock_base_transformer.fit.assert_called()

    def test_construction_calls_load(self):
        self.model
        self.mock_base_transformer.load.assert_called()

    def test_job_id_is_provided_job_id(self):
        self.assertEqual(self.job_id, self.model.job_id)

    def test_new_transformer_returns_default_model_index(self):
        self.assertEqual('model_0', self.model.new_transformer(None))

    def test_predict_returns_transformed_data(self):
        predicted_results = Mock()
        self.mock_base_transformer.transformed_data = ConditionalReturn()
        self.mock_base_transformer.transformed_data.return_when(predicted_results, *self.fake_args, **self.fake_kwargs)

        self.assertEqual(predicted_results, self.model.predict(*self.fake_args, **self.fake_kwargs))