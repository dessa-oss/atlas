"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from flask import request, make_response, Response

class APIResourceBuilder(object):

    def __init__(self, app_manager, klass, base_path):
        self._app_manager = app_manager
        self._klass = klass
        self._base_path = base_path
        self._api_actions = {}

    def _load_index_route(self):
        if hasattr(self._klass, 'index'):
            self._api_actions['get'] = self._get_api_index()
    
    def _load_post_route(self):
        if hasattr(self._klass, 'post'):
            self._api_actions['post'] = self._post_api_create()
    
    def _load_put_route(self):
        if hasattr(self._klass, 'put'):
            self._api_actions['put'] = self._put_api_create()

    def _create_action(self):
        self._load_index_route()
        self._load_post_route()
        self._load_put_route()
        resource_class = self._create_api_resource()
        self._add_resource(resource_class)

    def _add_resource(self, resource_class):
        self._app_manager.api().add_resource(resource_class, self._base_path)

    def _create_api_resource(self):
        from flask_restful import Resource
        import random

        class_name = '_%08x' % random.getrandbits(32)
        return type(class_name, (Resource,), self._api_actions)

    def _get_request_handler(self, method_name):

        def request_handler(resource, **kwargs):
            instance = self._klass()
            instance.params = self._api_params(kwargs)
            if hasattr(instance, 'json'):
                instance.params.update(request.json)
            method = getattr(instance, method_name)
            response = method()
            return response.as_json(), response.status()

        return request_handler

    def _get_api_index(self):
        return self._get_request_handler('index')

    def _post_api_create(self):
        return self._get_request_handler('post')

    def _put_api_create(self):
        return self._get_request_handler('put')

    def _api_params(self, kwargs):
        from flask import request

        params = dict(kwargs)
        dict_args = request.args.to_dict(flat=False)
        for key, value in dict_args.items():
            params[key] = value if len(value) > 1 else value[0]
        return params

def api_resource(base_path):

    def _make_api_resource(klass):
        """Decorator for defining resource for controllers
        """
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        rest_api_server = get_rest_api_server()
        APIResourceBuilder(rest_api_server, klass, base_path)._create_action()
        return klass

    return _make_api_resource