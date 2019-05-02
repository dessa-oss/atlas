"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.model_class import Model

class TestModel(Spec):

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
    
    @let_now
    def load_archive(self):
        load_archive = self.patch('foundations_contrib.archiving.load_archive', ConditionalReturn())
        load_archive.return_when(self.artifact_archive, 'artifact_archive')
        return load_archive

    @let
    def transformer_args(self):
        return self.faker.words()

    @let
    def transformer_kwargs(self):
        return self.faker.pydict()

    user_transformer = let_mock()
    
    @let_now
    def user_transformer_class(self):
        klass = ConditionalReturn()
        klass.return_when(self.user_transformer, *self.transformer_args, **self.transformer_kwargs)
        return klass

    def user_transformer_class_constructor(self, *args, **kwargs):
        return self.user_transformer_class(*args, **kwargs)

    mock_base_transformer = let_mock()

    def create_base_transformer_callback(self, model, user_transformer_stage):
        self.assertIsInstance(model, Model)
        self.assertEqual(self.user_transformer, user_transformer_stage.run_same_process())
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
        return Model(self.user_transformer_class_constructor, *self.transformer_args, **self.transformer_kwargs)

    def test_job_id_is_a_stage_that_returns_the_job_id_of_the_foundations_context(self):
        self.assertEqual(self.job_id, self.model.job_id.run_same_process())

    def test_new_transformer_returns_default_model_index(self):
        self.assertEqual('model_0', self.model.new_transformer(None))

    def test_fit_calls_fit_on_base_transformer_with_given_arguments(self):
        self.model.fit(*self.fake_args, **self.fake_kwargs)
        self.mock_base_transformer.fit.assert_called_with(*self.fake_args, **self.fake_kwargs)

    def test_fit_returns_transformer_encoder(self):
        result = self.model.fit(*self.fake_args, **self.fake_kwargs)
        self.assertEqual(self.mock_base_transformer.encoder(), result)

    def test_predict_returns_transformed_data(self):
        predicted_results = Mock()
        self.mock_base_transformer.transformed_data = ConditionalReturn()
        self.mock_base_transformer.transformed_data.return_when(predicted_results, *self.fake_args, **self.fake_kwargs)

        self.assertEqual(predicted_results, self.model.predict(*self.fake_args, **self.fake_kwargs))
    
    def test_encoder_returns_encoder(self):
        self.assertEqual(self.mock_base_transformer.encoder(), self.model.encoder())
