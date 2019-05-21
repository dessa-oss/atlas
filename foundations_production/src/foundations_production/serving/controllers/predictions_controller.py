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

@api_resource('/v1/<user_defined_model_name>/predictions/')
class PredictionsController(ControllerMixin):

    def get(self):
        
        @exceptions_as_http_errors
        def callback():
            return 'response'
        return Response('get_predictions_results', LazyResult(callback), status=200)

    def put(self):

        @exceptions_as_http_errors
        def callback():
            model_package_id = self._get_model_id_from_model_package_mapping()
            communicator = self._get_package_pool_communicator(model_package_id)
            communicator.set_action_request(self.params)
            predictions = communicator.get_response()
            self._raise_exception_if_available(predictions)
            return predictions
        return Response('do_predictions', LazyResult(callback), status=200)

    def _raise_exception_if_available(self, predictions):
        if predictions.get('name'):
            raise eval(predictions['name'])

    def _get_package_pool_communicator(self, model_package_id):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        rest_api_server = get_rest_api_server()
        package_pool = rest_api_server.get_package_pool()
        return package_pool.get_communicator(model_package_id)
