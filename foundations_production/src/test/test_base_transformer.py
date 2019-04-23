"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *


class TestBaseTransformer(Spec):

    preprocessor = let_mock()
    transformation = let_mock()
    mock_data = let_mock()
    mock_data_two = let_mock()

    @let
    def columns(self):
        return self.faker.words()

    @let
    def transformer(self):
        from foundations_production.base_transformer import BaseTransformer
        return BaseTransformer(self.preprocessor, self.columns, self.transformation)

    @set_up
    def set_up(self):
        self._fit_data = None
        self.transformation.fit.side_effect = self._fit_transformation
    
    def test_encoder_raises_value_error_when_not_fit(self):
        with self.assertRaises(ValueError) as context:
            self.transformer.encoder()
        self.assertIn('Transformer has not been fit. Call #fit() before using with encoder.', context.exception.args)

    def test_encoder_returns_fitted_transformation_when_fit_called(self):
        self.transformer.fit(self.mock_data)
        stage = self.transformer.encoder()
        stage.run_same_process()

        self.assertEqual(self.mock_data, self._fit_data)

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

    def _fit_transformation(self, data):
        self._fit_data = data