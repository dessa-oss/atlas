"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from .exceptions import AuthError

class AppManager:
    """A class to manage the initilization of the Flask server."""

    def __init__(self):
        self._app = None
        self._api = None

    def app(self):
        """Create and instantiate Flask object
        """
        from flask import Flask, jsonify
        from flask_cors import CORS

        if self._app is None:
            app = Flask(__name__)

            @app.errorhandler(AuthError)
            def handle_auth_error(exc):
                response = jsonify(exc.error)
                response.status_code = exc.status_code
                return response

            print('SPEC ======> ', app.error_handler_spec)
            self._app = app
            CORS(self._app, supports_credentials=True)

        return self._app

    def api(self):
        from flask_restful import Api

        if self._api is None:
            self._api = Api(self.app())
        return self._api
