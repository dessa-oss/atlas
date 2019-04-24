"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.model import Model

class TestModel(Spec):

    global_preprocessor = let_patch_mock('foundations_production.preprocessor_class.Preprocessor.active_preprocessor')
    global_model_package = let_patch_mock('foundations_production.model_package')

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

    @let_now
    def persister(self):
        instance = Mock()
        klass = self.patch('foundations_production.persister.Persister', ConditionalReturn())
        klass.return_when(instance, self.global_model_package)
        return instance

    fake_training_inputs = let_mock()
    fake_training_targets = let_mock()
    fake_validation_inputs = let_mock()
    fake_validation_targets = let_mock()

    @let_now
    def base_transformer(self):
        instance = Mock()
        klass = self.patch('foundations_production.base_transformer.BaseTransformer', ConditionalReturn())
        klass.return_when(instance, self.global_preprocessor, self.persister, self.user_transformer)
        return instance

    @let_now
    def mock_transform(self):
        self.base_transformer.transformed_data = ConditionalReturn()
        return self.base_transformer.transformed_data

    @let
    def transformer(self):
        return Model(self.user_transformer_class, *self.transformer_args, **self.transformer_kwargs)

    @set_up
    def set_up(self):
        self.mock_transform.return_when(self.fake_validation_targets, self.fake_validation_inputs)
          
    def test_fit_fits_selected_columns(self):
        self.transformer.fit(
            self.fake_training_inputs, 
            self.fake_training_targets, 
            self.fake_validation_inputs, 
            self.fake_validation_targets
        )

        self.base_transformer.fit.assert_called_with(
            self.fake_training_inputs, 
            self.fake_training_targets, 
            self.fake_validation_inputs, 
            self.fake_validation_targets
        )
    
    def test_transform_transforms_selected_columns(self):
        self.assertEqual(self.fake_validation_targets, self.transformer.predict(self.fake_validation_inputs))
