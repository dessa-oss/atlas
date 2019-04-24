"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import random

class TestBaseTransformer(Spec):

    preprocessor = let_mock()
    transformation = let_mock()
    mock_data = let_mock()
    mock_data_two = let_mock() 
    persister = let_mock()
    loaded_tranformation = let_mock()

    @let
    def transformer_index(self):
        return self.faker.random_int()

    @set_up
    def set_up(self):
        from foundations_production.base_transformer import BaseTransformer

        self._fit_data = None
        self.transformation.fit.side_effect = self._fit_transformation
        self.transformation.transform.side_effect = self._transformed_transformation
        self.preprocessor.new_transformer.return_value = self.transformer_index
        self.transformer = BaseTransformer(self.preprocessor, self.persister, self.transformation)

    def test_encoder_raises_value_error_when_not_fit(self):
        with self.assertRaises(ValueError) as context:
            self.transformer.encoder()
        self.assertIn('Transformer has not been fit. Call #fit() before using with encoder.', context.exception.args)

    def test_encoder_returns_fitted_transformation_when_fit_called(self):
        self.transformer.fit(self.mock_data)
        stage = self.transformer.encoder()
        stage.run_same_process()

        self.assertEqual(self.mock_data, self._fit_data)

    def test_encoder_stage_persists_fitted_transformation_when_run(self):
        self.transformer.fit(self.mock_data)
        stage = self.transformer.encoder()
        stage.run_same_process()

        self.persister.save_transformation.assert_called_with(self.transformer_index, self.transformation)

    def test_encoder_stage_loads_transformation_from_persister_when_load_called(self):
        self.transformer.fit(self.mock_data)
        self.transformer.load()
        stage = self.transformer.encoder()
        stage.run_same_process()

        self.persister.load_transformation.assert_called_with(self.transformer_index)

    def test_encoder_stage_returns_loaded_transformation_when_load_called(self):
        self.persister.load_transformation.return_value = self.loaded_tranformation
        
        self.transformer.fit(self.mock_data)
        self.transformer.load()
        
        stage = self.transformer.encoder()

        self.assertEqual(self.loaded_tranformation, stage.run_same_process())

    def test_trasformer_fit_is_not_called_when_load_is_called(self):
        self.transformer.fit(self.mock_data)
        self.transformer.load()
        stage = self.transformer.encoder()
        stage.run_same_process()

        self.transformation.fit.assert_not_called()
 
    def test_encoder_stage_returns_transformation_when_run(self):
        self.transformer.fit(self.mock_data)
        stage = self.transformer.encoder()
        self.assertEqual(self.transformation, stage.run_same_process())

    def test_running_encoder_stage_twice_calls_fit_once(self):
        self.transformer.fit(self.mock_data)

        self.transformer.encoder().run_same_process()
        self.transformer.encoder().run_same_process()

        self.transformation.fit.assert_called_once()

    def test_fitting_only_fits_once(self):
        self.transformer.fit(self.mock_data)
        self.transformer.fit(self.mock_data_two)

        self.transformer.encoder().run_same_process()

        self.assertEqual(self.mock_data, self._fit_data)

    def test_running_transform_returns_stage_that_encodes_data(self):
        training_data = random.randint(0, 100)
        validation_data = random.randint(0, 100)
        transformed_training_data = training_data + validation_data

        self.transformer.fit(training_data)
        encoding_stage = self.transformer.transformed_data(validation_data)

        self.assertEqual(transformed_training_data, encoding_stage.run_same_process())
    
    def test_base_transformer_registers_itself_with_preprocessor_when_constructed(self):
        self.preprocessor.new_transformer.assert_called_with(self.transformer)

    def _transformed_transformation(self, data):
        return self._fit_data + data

    def _fit_transformation(self, data):
        self._fit_data = data