"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class APIResourceBuilder(object):

    def __init__(self, klass, base_path):
        self._klass = klass
        self._base_path = base_path

    def _create_index_route(self):
        if hasattr(self._klass, 'index'):
            resource_class = self._create_api_resource()
            self._add_resource(resource_class)

    def _add_resource(self, resource_class):
        from foundations_rest_api.global_state import app_manager
        app_manager.api().add_resource(resource_class, self._base_path)

    def _create_api_resource(self):
        from flask_restful import Resource
        import random

        class_name = '_%08x' % random.getrandbits(32)
        return type(class_name, (Resource,), {'get': self._get_api_index()})

    def _get_api_index(self):
        def _get(resource_self, **kwargs):
            instance = self._klass()
            instance.params = self._api_params(kwargs)

            return instance.index().as_json()
        return _get

    def _api_params(self, kwargs):
        from flask import request

        params = dict(kwargs)
        dict_args = dict(request.args)
        for key, value in dict_args.items():
            params[key] = value if len(
                value) > 1 else value[0]
        return params

def api_resource(base_path):
    def _make_api_resource(klass):
        """Decorator for defining resource for controllers
        """
        APIResourceBuilder(klass, base_path)._create_index_route()
        return klass

    return _make_api_resource