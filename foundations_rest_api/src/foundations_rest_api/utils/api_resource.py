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
        from flask_restful import Resource
        from foundations_rest_api.global_state import app_manager
        from flask_restful import Resource

        import random

        if hasattr(klass, 'index'):
            def _get(self, **kwargs):
                from flask import request

                instance = klass()
                instance.params = dict(kwargs)
                dict_args = dict(request.args)
                for key, value in dict_args.items():
                    instance.params[key] = value if len(
                        value) > 1 else value[0]

                return instance.index().as_json()

            class_name = '_%08x' % random.getrandbits(32)
            resource_class = type(class_name, (Resource,), {'get': _get})
            app_manager.api().add_resource(resource_class, base_path)

        return klass
    return _make_api_resource