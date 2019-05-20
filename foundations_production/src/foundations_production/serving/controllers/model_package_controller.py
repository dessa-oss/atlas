"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_rest_api.response import Response
from foundations_rest_api.lazy_result import LazyResult
from foundations_production.serving.api_resource import api_resource
from foundations_production.serving.controllers.exceptions_as_http_errors import exceptions_as_http_errors
from foundations_production.serving.controllers.controller_mixin import ControllerMixin


@api_resource('/v1/<user_defined_model_name>/')
class ModelPackageController(ControllerMixin):

    def get(self):

        @exceptions_as_http_errors
        def callback():
            model_package_id = self._get_model_id_from_model_package_mapping()
            return {'model_id': model_package_id}

        return Response('get_model_package_id', LazyResult(callback), status=200)

    def post(self):

        @exceptions_as_http_errors
        def callback():
            from foundations_production.serving.rest_api_server_provider import get_rest_api_server

            rest_api_server = get_rest_api_server()
            model_package_mapping = rest_api_server.get_model_package_mapping()
            package_pool = rest_api_server.get_package_pool()
            model_id = self.params['model_id']
            user_defined_model_name = self.params['user_defined_model_name']

            package_pool.add_package(model_id)
            model_package_mapping[user_defined_model_name] = model_id
            return {'deployed_model_id': model_id}

        return Response('create_model_package_controller', LazyResult(callback), status=201)

    def delete(self):

        @exceptions_as_http_errors
        def callback():
            return 'deleted'

        return Response('delete_model_package', LazyResult(callback), status=200)
