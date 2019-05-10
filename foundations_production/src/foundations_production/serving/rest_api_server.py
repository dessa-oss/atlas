"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
class RestAPIServer(object):

    def __init__(self):
        from flask import Flask
        from foundations_production.serving.package_pool import PackagePool

        self._package_pool = PackagePool(1000)
        self._flask = Flask(__name__)
        self._register_routes(self._flask)

    def exceptions_as_http_error_codes(method):
        from functools import wraps

        @wraps(method)
        def method_decorator(*args, **kwargs):
            from flask import request, abort

            try:
                return method(*args, **kwargs)
            except KeyError:
                abort(400)

        return method_decorator

    @property
    def flask(self):
        return self._flask

    def run(self):
        self._flask.run()
        
    def _register_routes(self, flask):

        @flask.before_request
        def accept_only_json():
            from flask import request, abort

            if not request.is_json: 
                abort(400)
        
        flask.add_url_rule('/v1/<user_defined_model_name>/', methods=['GET', 'POST', 'DELETE', 'HEAD'], view_func=self.manage_model_package)
        flask.add_url_rule('/v1/<user_defined_model_name>/model/', methods=['GET', 'PUT', 'HEAD'], view_func=self.train_all_model_packages)
        flask.add_url_rule('/v1/<user_defined_model_name>/model/<version>', methods=['GET', 'PUT', 'HEAD'], view_func=self.train_one_model_package)
        flask.add_url_rule('/v1/<user_defined_model_name>/predictions', methods=['GET', 'POST', 'HEAD'], view_func=self.predictions_from_model_package)
        flask.add_url_rule('/v1/<user_defined_model_name>/predictions/<prediction_id>', methods=['GET', 'HEAD'], view_func=self.predict_with_model_package)

    @exceptions_as_http_error_codes
    def manage_model_package(self, user_defined_model_name):
        from flask import request, jsonify
        
        model_id = request.get_json()['model_id']
        self._package_pool.add_package(model_id)
        return 'response'

    @exceptions_as_http_error_codes
    def train_all_model_packages(self, user_defined_model_name):
        return 'response'

    @exceptions_as_http_error_codes
    def train_one_model_package(self, user_defined_model_name, version):
        return 'response'

    @exceptions_as_http_error_codes
    def predictions_from_model_package(self, user_defined_model_name):
        return 'response'

    @exceptions_as_http_error_codes
    def predict_with_model_package(self, user_defined_model_name, prediction_id):
        return 'response'
