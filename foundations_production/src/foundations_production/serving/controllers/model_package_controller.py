"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_production.serving.api_resource import api_resource
from foundations_rest_api.response import Response
from foundations_rest_api.lazy_result import LazyResult

@api_resource('/v1/<user_defined_model_name>/')
class ModelPackageController(object):

    def get(self):
        if not self._model_package_exists():
            return Response.constant('model package not found', status=404)
        return Response.constant('response')

    def post(self):
        def callback():
            from foundations_production.serving.rest_api_server_provider import get_rest_api_server

            rest_api_server = get_rest_api_server()
            model_package_mapping = rest_api_server.get_module_package_mapping()
            package_pool = rest_api_server.get_package_pool()
            model_id = self.params['model_id']
            user_defined_model_name = self.params['user_defined_model_name']

            package_pool.add_package(model_id)
            model_package_mapping[user_defined_model_name] = model_id
            return {'deployed_model_id': model_id}

        return Response('create_model_package_controller', LazyResult(callback), status=201)

    def delete(self):
        return Response.constant('deleted')

    def _model_package_exists(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        rest_api_server = get_rest_api_server()
        model_package_mapping = rest_api_server.get_module_package_mapping()
        return self.params['user_defined_model_name'] in model_package_mapping
