"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class AppManager(object):
    """A class to manage the initilization of the Flask server.
        Arguments:
            
    """    
    def __init__(self):
        self._app = None
        self._api = None

    def app(self):
        """Create and instantiate Flask object
        """
        from flask import Flask
        from flask_cors import CORS

        if self._app is None:
            self._app = Flask(__name__)
            CORS(self._app)

        return self._app

    def api(self):
        from flask_restful import Api

        if self._api is None:
            self._api = Api(self.app())
        return self._api