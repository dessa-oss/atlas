"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
class APIResourceBuilder(object):

    def __init__(self, app_manager, klass, base_path):
        self._app_manager = app_manager
        self._klass = klass
        self._base_path = base_path
        self._api_actions = {}

    def _load_route(self, method_name):
        if hasattr(self._klass, method_name):
            self._api_actions[method_name] = self._get_request_handler(method_name)
        else:
            self._api_actions[method_name] = self._get_default_api_response()

    def _create_action(self):
        for method_name in ['get', 'post', 'put', 'patch', 'delete']:
            self._load_route(method_name)
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
            from flask import request

            instance = self._klass()
            instance.params = self._api_params(kwargs)
            if getattr(request, 'json'):
                instance.params.update(request.json)
            method = getattr(instance, method_name)
            response = method()
            response_data = self.exceptions_as_http_error_codes(response.as_json)()
            status_code = response.status()
            return response_data, status_code

        return request_handler

    def _get_default_api_response(self):
        def default_request_handler(resource, **kwargs):
            from werkzeug.exceptions import MethodNotAllowed
            raise MethodNotAllowed()
        return default_request_handler

    def _api_params(self, kwargs):
        from flask import request

        params = dict(kwargs)
        dict_args = request.args.to_dict(flat=False)
        for key, value in dict_args.items():
            params[key] = value if len(value) > 1 else value[0]
        return params

    def exceptions_as_http_error_codes(self, method):
        from functools import wraps

        @wraps(method)
        def method_decorator(*args, **kwargs):
            from flask import request, abort
            from werkzeug.exceptions import BadRequestKeyError

            try:
                return method(*args, **kwargs)
            except KeyError as exception:
                missing_key = exception.args[0]
                raise BadRequestKeyError(description='Missing field in JSON data: {}'.format(missing_key))
            except Exception:
                abort(500)

        return method_decorator


def api_resource(base_path):

    def _make_api_resource(klass):
        """Decorator for defining resource for controllers
        """
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        rest_api_server = get_rest_api_server()
        APIResourceBuilder(rest_api_server, klass, base_path)._create_action()
        return klass

    return _make_api_resource
