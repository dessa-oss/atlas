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
        self._app = Flask(__name__)
        self._load_routes(self._app)


    def exceptions_as_http_error_codes(method):

        def method_decorator(*args, **kwargs):
            from flask import request, abort

            try:
                return method(*args, **kwargs)
            except KeyError:
                abort(400)

        return method_decorator

    @property
    def app(self):
        return self._app

    def run(self):
        self._app.run()
        
    def _load_routes(self, flask_app):

        @flask_app.before_request
        def accept_only_json():
            from flask import request, abort

            if not request.is_json: 
                abort(400)

        @flask_app.route('/v1/<user_defined_model_name>/', methods=['GET', 'POST', 'DELETE', 'HEAD'])
        def manage_model_package(user_defined_model_name):
            return self._manage_model_package(user_defined_model_name)

        @flask_app.route('/v1/<user_defined_model_name>/model/', methods=['GET', 'PUT', 'HEAD'])
        def train_all_model_packages(user_defined_model_name):
            return self._train_all_model_packages(user_defined_model_name)

        @flask_app.route('/v1/<user_defined_model_name>/model/<version>', methods=['GET', 'PUT', 'HEAD'])
        def train_one_model_package(user_defined_model_name, version):
            return self._train_one_model_package(user_defined_model_name, version)

        @flask_app.route('/v1/<user_defined_model_name>/predictions', methods=['GET', 'POST', 'HEAD'])
        def predictions_from_model_package(user_defined_model_name):
            return self._predictions_from_model_package(user_defined_model_name)

        @flask_app.route('/v1/<user_defined_model_name>/predictions/<prediction_id>', methods=['GET', 'HEAD'])
        def predict_with_model_package(user_defined_model_name, prediction_id):
            return self._predict_with_model_package(user_defined_model_name, prediction_id)

    @exceptions_as_http_error_codes
    def _manage_model_package(self, user_defined_model_name):
        from flask import request, jsonify
        
        model_id = request.get_json()['model_id']
        self._package_pool.add_package(model_id)
        return 'response'

    @exceptions_as_http_error_codes
    def _train_all_model_packages(self, user_defined_model_name):
        return 'response'

    @exceptions_as_http_error_codes
    def _train_one_model_package(self, user_defined_model_name, version):
        return 'response'

    @exceptions_as_http_error_codes
    def _predictions_from_model_package(self, user_defined_model_name):
        return 'response'

    @exceptions_as_http_error_codes
    def _predict_with_model_package(self, user_defined_model_name, prediction_id):
        return 'response'
