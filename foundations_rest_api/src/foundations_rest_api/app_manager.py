"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class AppManager(object):
    def __init__(self):
        self._app = None

    def app(self):
        from flask import Flask

        if self._app is None:
            self._app = Flask(__name__)

        return self._app
