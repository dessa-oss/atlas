"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

def load_routes(flask_app):
    from flask import request
    
    @flask_app.route('/v1/<user_defined_model_name>', methods=[])
    def manage_model_package(user_defined_model_name):
        pass

    @flask_app.route('/v1/<user_defined_model_name>/model', methods=[])
    def train_all_model_packages(user_defined_model_name):
        pass

    @flask_app.route('/v1/<user_defined_model_name>/model/<version>', methods=[])
    def train_one_model_package(user_defined_model_name):
        pass

    @flask_app.route('/v1/<user_defined_model_name>/predictions', methods=[])
    def predictions_from_model_package(user_defined_model_name):
        pass

    @flask_app.route('/v1/<user_defined_model_name>/predictions/<id>', methods=[])
    def predict_with_model_package(user_defined_model_name):
        pass