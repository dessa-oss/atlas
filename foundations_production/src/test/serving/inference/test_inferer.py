"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


from foundations_spec import *

from foundations import create_stage
from foundations_production import preprocessor
from foundations_production.model_class import Model
from foundations_production.serving.inference.inferer import Inferer

class TestInferer(Spec):

    model_package = let_mock()
    input_data = let_mock()
    transformed_input_data = let_mock()
    predictions = let_mock()

    @let
    def model(self):
        model = Mock()
        model.predict = create_stage(self._predict)
        return model

    @let
    def predict_callback(self):
        callback = ConditionalReturn()
        callback.return_when(self.predictions, self.transformed_input_data)
        return callback

    @let
    def preprocessor_callback(self):
        callback = ConditionalReturn()
        callback.return_when(self.transformed_input_data, self.input_data)
        return callback
    
    @let
    def inferer(self):
        return Inferer(self.model_package)

    @set_up
    def set_up(self):
        self.model_package.preprocessor = self._preprocessor
        self.model_package.model = self.model

    def test_predictions_for_returns_predictions_for_input_data(self):
        self.assertEqual(self.predictions, self.inferer.predictions_for(self.input_data))

    def _preprocessor(self, input):
        return self.preprocessor_callback(input)
    
    def _predict(self, input):
        return self.predict_callback(input)