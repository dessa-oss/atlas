"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def api_resource(base_path):
    def _make_api_resource(klass):
        """Decorator for defining resource for controllers
        """
        _create_index_route(klass, base_path)
        return klass

    return _make_api_resource

def _create_index_route(klass, base_path):
    if hasattr(klass, 'index'):
        resource_class = _create_api_resource(klass)
        _add_resource(resource_class, base_path)

def _add_resource(resource_class, base_path):
    from foundations_rest_api.global_state import app_manager
    app_manager.api().add_resource(resource_class, base_path)

def _create_api_resource(klass):
    from flask_restful import Resource
    import random

    class_name = '_%08x' % random.getrandbits(32)
    return type(class_name, (Resource,), {'get': _get_api_index(klass)})

def _get_api_index(klass):
    def _get(self, **kwargs):
        instance = klass()
        instance.params = _api_params(kwargs)

        return instance.index().as_json()
    return _get

def _api_params(kwargs):
    from flask import request

    params = dict(kwargs)
    dict_args = dict(request.args)
    for key, value in dict_args.items():
        params[key] = value if len(
            value) > 1 else value[0]
    return params
