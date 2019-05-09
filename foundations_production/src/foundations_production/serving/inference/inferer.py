"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


class Inferer(object):
    
    def __init__(self, model_package):
        self._model_package = model_package

    def predictions_for(self, input_data):
        transformed_data = self._preprocessed_data(input_data)
        predictions = self._model_predictions(transformed_data)
        return predictions.run_same_process()

    def __eq__(self, rhs):
        return self._model_package == rhs._model_package
        
    def _preprocessed_data(self, input_data):
        return self._model_package.preprocessor(input_data)
    
    def _model_predictions(self, transformed_data):
        return self._model_package.model.predict(transformed_data)