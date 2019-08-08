"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def prediction_resource(prediction_callback):
    from flask import request
    from flask_restful import Resource

    from uuid import uuid4

    class _PredictionResource(Resource):

        def get(self):
            return {'message': 'still alive'}

        def post(self):
            callback_kwargs = dict(request.json)
            return prediction_callback(**callback_kwargs)

    _PredictionResource.__name__ = f'_PredictionResource_{uuid4()}'

    return _PredictionResource