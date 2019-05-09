"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


from foundations_spec import *
from foundations_production import preprocessor
from foundations_production.model_class import Model
from foundations_production.serving.inference.data_frame_parser import DataFrameParser
from foundations_production.serving.inference.inferer import Inferer
from foundations_production.model_package import ModelPackage
from foundations import create_stage

class TestCanPerformInference(Spec):

    class FakeModel(object):

        def __init__(self):
            self.predict = create_stage(self._predict)

        @staticmethod
        def _predict(input):
            input['1st column'] += ' predicted'
            input['2nd column'] += 100
            return input

    @let
    def input(self):
        return {
            'rows': [['value', 43234], ['spider', 323]], 
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }

    @let
    def preprocessor(self):
        @create_stage
        def _preprocessor(input):
            input['1st column'] += ' transformed'
            input['2nd column'] += 333
            return input
        return _preprocessor

    @let
    def data_frame_parser(self):
        return DataFrameParser()

    @let
    def model(self):
        return self.FakeModel()

    @let
    def model_package(self):
        return ModelPackage(model=self.model, preprocessor=self.preprocessor)

    @let
    def inferer(self):
        return Inferer(self.model_package)

    def test_can_perform_inference(self):
        input_data_frame = self.data_frame_parser.data_frame_for(self.input)
        predictions_data_frame = self.inferer.predictions_for(input_data_frame)
        jsonified_data_frame = self.data_frame_parser.data_frame_as_json(predictions_data_frame)
        self.assertEqual({
            'rows': [['value transformed predicted', 43667], ['spider transformed predicted', 756]], 
            'schema': [{'name': '1st column', 'type': 'object'}, {'name': '2nd column', 'type': 'int64'}]
        }, jsonified_data_frame)