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
    current_foundations_context = let_patch_mock('foundations_production.model_class.current_foundations_context')
    pipeline_archiver = let_mock()
    artifact_archive = let_mock()

    @let_now
    def foundations_context(self):
        return self.current_foundations_context.return_value

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

    @let
    def fake_data_from_stage(self):
        import foundations
        
        def fake_data():
            return self.fake_retraining_data

        return foundations.create_stage(fake_data)()

    @let
    def fake_retraining_data(self):
        return self.faker.sentence()

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

    def test_retrain_prepares_model_for_retrain(self):
        self.model.retrain(*self.fake_args, **self.fake_kwargs)
        self.mock_base_transformer.prepare_for_retrain.assert_called_once()

    def test_retrain_loads_and_fits_model_with_new_data(self):
        self.mock_base_transformer.fit = ConditionalReturn()
        self.mock_base_transformer.fit.return_when(None)
        self.mock_base_transformer.fit.return_when(None, *self.fake_args, **self.fake_kwargs)
        
        fit_stage = self.model.retrain(*self.fake_args, **self.fake_kwargs)
        self.assertEqual(self.mock_base_transformer.encoder(), fit_stage)

    def test_encoder_returns_encoder(self):
        self.assertEqual(self.mock_base_transformer.encoder(), self.model.encoder())