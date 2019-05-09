"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


class Predictor(object):
    
    @staticmethod
    def predictor_for(model_package_id):
        from foundations_production import load_model_package
        
        model_package = load_model_package(model_package_id)
        return Predictor(model_package)

    def __init__(self, model_package):
        self._model_package = model_package

    def json_predictions_for(self, json_inputs):
        pass

    def __eq__(self, rhs):
        return self._model_package == rhs._model_package