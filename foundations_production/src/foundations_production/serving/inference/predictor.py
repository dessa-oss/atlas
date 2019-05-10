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
        from foundations_production.serving.inference.inferer import Inferer
        
        model_package = load_model_package(model_package_id)
        inferer = Inferer(model_package)
        return Predictor(inferer)

    def __init__(self, inferer):
        self._inferer = inferer

    def json_predictions_for(self, json_inputs):
        from foundations_production.serving.inference.data_frame_parser import DataFrameParser
        dataframe_inputs = DataFrameParser().data_frame_for(json_inputs)
        self._inferer.predictions_for(dataframe_inputs)
 

    def __eq__(self, rhs):
        return self._inferer == rhs._inferer