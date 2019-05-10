"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


from foundations_spec import *
from foundations_production.serving.inference.predictor import Predictor

class TestPredictor(Spec):

    model_package = let_mock()
    inferer = let_mock()

    @let
    def input(self):
        return {
            'rows': [['value', 43234], ['spider', 323]], 
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }

    @let
    def model_package_id(self):
        return self.faker.uuid4()

    @let_now
    def mock_load_model_package(self):
        mock = self.patch('foundations_production.load_model_package', ConditionalReturn())
        mock.return_when(self.model_package, self.model_package_id)
        return mock

    @let
    def predictor(self):
        return Predictor(self.inferer)
    
    def test_predictors_with_same_model_package_are_the_same_predictor(self):
        rhs = Predictor(self.inferer)
        self.assertEqual(rhs, self.predictor)

    def test_predictors_with_diff_inferer_are_diff_predictors(self):
        rhs_inferer = Mock()
        rhs = Predictor(rhs_inferer)
        self.assertNotEqual(rhs, self.predictor)

    def test_predictor_for_returns_predictor_for_requested_model_package_id(self):
        from foundations_production.serving.inference.inferer import Inferer

        expected_predictor = Predictor(Inferer(self.model_package))
        self.assertEqual(expected_predictor, Predictor.predictor_for(self.model_package_id))
    
    def test_json_predictions_for_coverts_json_input_data_into_dataframe(self):
        mock_data_frame_parser = self.patch('foundations_production.serving.inference.data_frame_parser.DataFrameParser')
        self.predictor.json_predictions_for(self.input)
        mock_data_frame_parser.return_value.data_frame_for.assert_called_with(self.input)

