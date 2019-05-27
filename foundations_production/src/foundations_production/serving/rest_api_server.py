"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_production.serving.rest_api_server_provider import register_rest_api_server

class RestAPIServer(object):

    def __init__(self):
        from flask import Flask, got_request_exception
        from flask_restful import Api
        from foundations_production.serving.package_pool import PackagePool

        self._package_pool = PackagePool(1000)
        self._flask = Flask(__name__)
        self._flask.config['ERROR_404_HELP'] = False
        self._api = Api(self._flask)
        self._register_routes(self._flask)
        self._model_package_mapping = {}
        register_rest_api_server(self)

    @property
    def flask(self):
        return self._flask

    def api(self):
        return self._api

    def run(self, host='localhost', port=5000):
        self._flask.run(host=host, port=port)

    def get_model_package_mapping(self):
        return self._model_package_mapping

    def get_package_pool(self):
        return self._package_pool

    def _register_routes(self, flask):
        from werkzeug.exceptions import HTTPException
        from flask import jsonify

        @flask.before_request
        def accept_only_json():
            from flask import request, abort, jsonify, make_response

            if request.method in ['POST', 'PUT', 'PATCH'] and not request.is_json:
                abort(make_response(jsonify(message='Invalid content type'), 400))

        flask.add_url_rule('/v1/<user_defined_model_name>/predictions', methods=['GET', 'POST', 'HEAD'], view_func=self.predictions_from_model_package)

    def predictions_from_model_package(self, user_defined_model_name):
        from flask import make_response, request
        import json

        if request.method in ['GET', 'HEAD']:
            return 'response'

        model_id = self._model_package_mapping.get(user_defined_model_name)
        communicator = self._package_pool.get_communicator(model_id)
        communicator.set_action_request(request.get_json())
        predictions = communicator.get_response()
        if predictions.get('name'):
            raise eval(predictions['name'])

        response = make_response(json.dumps(predictions), 200)
        return response
