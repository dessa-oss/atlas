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

            self._app = app
            CORS(self._app, supports_credentials=True)

        return self._app

    def api(self):
        from flask_restful import Api

        if self._api is None:
            self._api = Api(self.app())
        return self._api
