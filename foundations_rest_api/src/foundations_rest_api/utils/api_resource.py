"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.app_manager import AppManager
from flask_restful import Api

app_manager = AppManager()
app = app_manager.app()

api = Api(app)


def api_resource(klass):
    from flask_restful import Resource

    if hasattr(klass, 'index'):
        def _get(self):
            return klass().index()
        resource_class = type('', (Resource,), {'get': _get})
        api.add_resource(resource_class, '/lou')

    return klass