"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def evaluate_resource(evaluate_callback):
    from flask import request
    from flask_restful import Resource
    from multiprocessing import Process

    from uuid import uuid4

    class _EvaluateResource(Resource):

        def post(self):
            if evaluate_callback is None:
                return {'error': 'evaluate not set in manifest'}, 404

            callback_kwargs = dict(request.json)
            process = Process(target=evaluate_callback, kwargs=callback_kwargs)
            process.start()

            return {}, 202

    _EvaluateResource.__name__ = f'_EvaluateResource_{uuid4()}'

    return _EvaluateResource