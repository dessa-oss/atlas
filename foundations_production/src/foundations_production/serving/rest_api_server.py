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

    @property
    def app(self):
        return self._app

    def run(self):
        self._app.run()
        
    def _load_routes(self, flask_app):
        from flask import request, abort, jsonify
        
        @flask_app.before_request
        def accept_only_json():
            if not request.is_json: 
                abort(400)

        @flask_app.route('/v1/<user_defined_model_name>/', methods=['GET', 'POST', 'DELETE', 'HEAD'])
        def manage_model_package(user_defined_model_name):
            try:
                model_id = request.get_json()['model_id']
                self._package_pool.add_package(model_id)
            except KeyError:
                abort(400)

        @flask_app.route('/v1/<user_defined_model_name>/model/', methods=['GET', 'PUT', 'HEAD'])
        def train_all_model_packages(user_defined_model_name):
            return 'response'

        @flask_app.route('/v1/<user_defined_model_name>/model/<version>', methods=['GET', 'PUT', 'HEAD'])
        def train_one_model_package(user_defined_model_name, version):
            return 'response'

        @flask_app.route('/v1/<user_defined_model_name>/predictions', methods=['GET', 'POST', 'HEAD'])
        def predictions_from_model_package(user_defined_model_name):
            return 'response'

        @flask_app.route('/v1/<user_defined_model_name>/predictions/<id>', methods=['GET', 'HEAD'])
        def predict_with_model_package(user_defined_model_name, id):
            return 'response'
