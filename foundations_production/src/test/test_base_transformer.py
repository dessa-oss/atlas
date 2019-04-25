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
    mock_data = let_mock()
    mock_data_two = let_mock() 
    persister = let_mock()
    loaded_tranformation = let_mock()

    mock_fit = let_mock()
    mock_transform = let_mock()

    @let
    def transformer_index(self):
        return self.faker.random_int()

    @let
    def construct_transformation(self):
        transformation = Mock()
        transformation.fit = self.mock_fit
        transformation.transform = self.mock_transform
        return transformation

    @let
    def transformation(self):
        import foundations

        def _construct_transformation():
            return self.construct_transformation
    
        return foundations.create_stage(_construct_transformation)()

    @set_up
    def set_up(self):
        from foundations_production.base_transformer import BaseTransformer

        self._fit_data = None
        self.mock_fit.side_effect = self._fit_transformation
        self.mock_transform.side_effect = self._transformed_transformation
        self.preprocessor.new_transformer.return_value = self.transformer_index
        self.transformer = BaseTransformer(self.preprocessor, self.persister, self.transformation)
        self._mock_fit_called = False

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

        self.persister.save_transformation.assert_called_with(self.transformer_index, self.construct_transformation)

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

        self.mock_fit.assert_not_called()

    def test_transformer_is_not_loaded_if_load_is_not_called(self):
        self.transformer.fit(self.mock_data)
        stage = self.transformer.encoder()
        stage.run_same_process()

        self.persister.load_transformation.assert_not_called()

    def test_do_not_save_transformation_when_load_is_called(self):
        self.transformer.fit(self.mock_data)
        self.transformer.load()
        stage = self.transformer.encoder()
        stage.run_same_process()

        self.persister.save_transformation.assert_not_called()

    def test_call_fit_before_save_transformation(self):

        def mock_save_transformation(transformer_index, transformation):
            if not self._mock_fit_called:
                raise AssertionError('transformation.fit() not called before persister.save_transformation()')
        
        self.persister.save_transformation = mock_save_transformation

        self.transformer.fit(self.mock_data)
        stage = self.transformer.encoder()
        stage.run_same_process()

    def test_encoder_stage_returns_transformation_when_run(self):
        self.transformer.fit(self.mock_data)
        stage = self.transformer.encoder()
        self.assertEqual(self.construct_transformation, stage.run_same_process())

    def test_running_encoder_stage_twice_calls_fit_once(self):
        self.transformer.fit(self.mock_data)

        self.transformer.encoder().run_same_process()
        self.transformer.encoder().run_same_process()

        self.mock_fit.assert_called_once()

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

    def test_fit_supports_arbitrary_arguments(self):
        self.mock_fit.side_effect = self._complex_fit_transformation

        args = tuple(self.faker.words())
        kwargs = self.faker.pydict()

        self.transformer.fit(*args, **kwargs)
        stage = self.transformer.encoder()
        stage.run_same_process()

        self.assertEqual((args, kwargs), self._fit_data)

    def test_transform_data_supports_arbitrary_arguments(self):
        self.mock_transform.side_effect = self._complex_transformed_transformation

        args = tuple(self.faker.words())
        kwargs = self.faker.pydict()

        self.transformer.fit(None)
        encoding_stage = self.transformer.transformed_data(*args, **kwargs)

        self.assertEqual((args, kwargs), encoding_stage.run_same_process())

    def _transformed_transformation(self, data):
        return self._fit_data + data

    def _complex_transformed_transformation(self, *args, **kwargs):
        return (args, kwargs)

    def _fit_transformation(self, data):
        self._mock_fit_called = True
        self._fit_data = data

    def _complex_fit_transformation(self, *args, **kwargs):
        self._fit_data = (args, kwargs)