"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_production.serving.controllers.exceptions_as_http_errors import exceptions_as_http_errors


class RestAPIServer(object):

    def __init__(self):
        from foundations_production.serving.package_pool import PackagePool

        self._setup_server()
        self._package_pool = PackagePool(1000)
        self._model_package_mapping = {}

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

    def _setup_server(self):
        from foundations_production.serving.rest_api_server_provider import register_rest_api_server

        self._initialize_flask_app()
        self._initialize_requests_handling()
        register_rest_api_server(self)

    def _initialize_flask_app(self):
        from flask import Flask
        from flask_restful import Api

        self._flask = Flask(__name__)
        self._flask.config['ERROR_404_HELP'] = False
        self._api = Api(self._flask)

    def _initialize_requests_handling(self):
        from werkzeug.exceptions import HTTPException
        from flask import jsonify

        flask_app = self._flask

        @flask_app.before_request
        def accept_only_json():
            from flask import request, abort, jsonify, make_response

            if request.method in ['POST', 'PUT', 'PATCH'] and not request.is_json:
                abort(make_response(jsonify(message='Invalid content type'), 400))
