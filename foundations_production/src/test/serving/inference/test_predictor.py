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
        return Predictor(self.model_package)
    
    def test_predictors_with_same_model_package_are_the_same_predictor(self):
        rhs = Predictor(self.model_package)
        self.assertEqual(rhs, self.predictor)

    def test_predictors_with_diff_model_package_are_diff_predictors(self):
        rhs_model_package = Mock()
        rhs = Predictor(rhs_model_package)
        self.assertNotEqual(rhs, self.predictor)

    def test_predictor_for_returns_predictor_for_requested_model_package_id(self):
        self.assertEqual(self.predictor, Predictor.predictor_for(self.model_package_id))