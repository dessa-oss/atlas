"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_production.serving.rest_api_server_provider import register_rest_api_server

class RestAPIServer(object):

    def __init__(self):
        from flask import Flask
        from flask_restful import Api
        from foundations_production.serving.package_pool import PackagePool

        self._package_pool = PackagePool(1000)
        self._flask = Flask(__name__)
        self._api = Api(self._flask)
        self._register_routes(self._flask)
        self._model_package_mapping = {}
        register_rest_api_server(self)

    def exceptions_as_http_error_codes(method):
        from functools import wraps

        @wraps(method)
        def method_decorator(*args, **kwargs):
            from flask import request, abort
            from werkzeug.exceptions import BadRequestKeyError

            try:
                return method(*args, **kwargs)
            except KeyError as exception:
                missing_key = exception.args[0]
                raise BadRequestKeyError(description='Missing field in JSON data: {}'.format(missing_key))
            except Exception:
                abort(500)

        return method_decorator

    @property
    def flask(self):
        return self._flask

    def api(self):
        return self._api

    def run(self, host='localhost', port=5000):
        self._flask.run(host=host, port=port)

    def get_module_package_mapping(self):
        return self._model_package_mapping

    def get_package_pool(self):
        return self._package_pool

    def _register_routes(self, flask):
        from werkzeug.exceptions import HTTPException
        from flask import jsonify

        @flask.before_request
        def accept_only_json():
            from flask import request, abort

            if request.method in ['POST', 'PUT', 'PATCH'] and not request.is_json:
                abort(400)

        @flask.errorhandler(HTTPException)
        def handle_exceptions(exception):
            return jsonify({'error': str(exception)}), exception.code, {'Content-Type': 'application/json'}


        flask.add_url_rule('/v1/<user_defined_model_name>/', methods=['GET', 'POST', 'DELETE', 'HEAD'], view_func=self.manage_model_package)
        flask.add_url_rule('/v1/<user_defined_model_name>/model/', methods=['GET', 'PUT', 'HEAD'], view_func=self.train_latest_model_package)
        flask.add_url_rule('/v1/<user_defined_model_name>/model/<version>', methods=['GET', 'PUT', 'HEAD'], view_func=self.train_one_model_package)
        flask.add_url_rule('/v1/<user_defined_model_name>/predictions', methods=['GET', 'POST', 'HEAD'], view_func=self.predictions_from_model_package)
        flask.add_url_rule('/v1/<user_defined_model_name>/predictions/<prediction_id>', methods=['GET', 'HEAD'], view_func=self.predict_with_model_package)

    @exceptions_as_http_error_codes
    def manage_model_package(self, user_defined_model_name):
        from flask import request, jsonify
        from flask import make_response
        
        if request.method == 'POST':
            model_id = request.get_json()['model_id']
            self._package_pool.add_package(model_id)
            self._model_package_mapping[user_defined_model_name] = model_id
            return jsonify({'deployed_model_id': model_id})

        return 'response'

    @exceptions_as_http_error_codes
    def train_latest_model_package(self, user_defined_model_name):
        from flask import request, jsonify, make_response
        from foundations_production.serving import create_retraining_job

        if user_defined_model_name not in self._model_package_mapping:
            return make_response('response', 404)

        if request.method in ['GET', 'HEAD']:
            return make_response('response', 200)

        targets_location, features_location = self._retraining_data_locations(request)

        model_package_id = self._model_package_id_from_name(user_defined_model_name)
        retraining_job_deployment = self._deploy_retraining_job(model_package_id, targets_location, features_location)
        response_body = self._response_body_with_retraining_job_id(retraining_job_deployment)

        return make_response(response_body, 202)

    def _deploy_retraining_job(self, model_package_id, targets_location, features_location):
        from foundations_production.serving import create_retraining_job

        retraining_job = create_retraining_job(model_package_id, targets_location=targets_location, features_location=features_location)
        return retraining_job.run()

    def _retraining_data_locations(self, request):
        request_body = request.get_json()
        features_location = request_body['features_file']
        targets_location = request_body['targets_file']
        
        return targets_location, features_location

    def _model_package_id_from_name(self, user_defined_model_name):
        return self._model_package_mapping[user_defined_model_name]

    def _response_body_with_retraining_job_id(self, retraining_job_deployment):
        from flask import jsonify
        return jsonify({'created_job_uuid': retraining_job_deployment.job_name()})

    @exceptions_as_http_error_codes
    def train_one_model_package(self, user_defined_model_name, version):
        return 'response'

    @exceptions_as_http_error_codes
    def predictions_from_model_package(self, user_defined_model_name):
        from flask import make_response, request
        import json

        model_id = self._model_package_mapping.get(user_defined_model_name)
        communicator = self._package_pool.get_communicator(model_id)
        communicator.set_action_request(request.get_json())
        predictions = communicator.get_response()
        if predictions.get('name'):
            raise eval(predictions['name'])

        response = make_response(json.dumps(predictions), 200)
        return response

    @exceptions_as_http_error_codes
    def predict_with_model_package(self, user_defined_model_name, prediction_id):
        return 'response'
