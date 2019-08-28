"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def flask_app(root_resource, predict_resource, evaluate_resource):
    from flask import Flask
    from flask_cors import CORS
    from flask_restful import Api

    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    api = Api(app)

    api.add_resource(root_resource, '/')
    api.add_resource(predict_resource, '/predict')
    api.add_resource(evaluate_resource, '/evaluate')
    # app.logger.disabled = True

    return app