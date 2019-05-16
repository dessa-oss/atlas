"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_production.serving.api_resource import api_resource

@api_resource('/v1/<user_defined_model_name>/')
class ModelPackageController(object):

    def post(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server
        from foundations_rest_api.response import Response
        from foundations_rest_api.lazy_result import LazyResult

        def callback():
            rest_api_server = get_rest_api_server()
            model_package_mapping = rest_api_server.get_module_package_mapping()
            package_pool = rest_api_server.get_package_pool()
            model_id = self.params['model_id']
            user_defined_model_name = self.params['user_defined_model_name']

            package_pool.add_package(model_id)
            model_package_mapping[user_defined_model_name] = model_id
            return {'deployed_model_id': model_id}

        return Response('model_package_controller_create', LazyResult(callback))