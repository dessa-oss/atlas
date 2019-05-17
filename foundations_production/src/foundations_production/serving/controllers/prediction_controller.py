"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_production.serving.api_resource import api_resource
from foundations_rest_api.response import Response
from foundations_rest_api.lazy_result import LazyResult

@api_resource('/v1/<user_defined_model_name>/predictions')
class PredictionController(object):

    def get(self):
        if not self._model_package_exists():
            return Response.constant('model package not found', status=404)
        return Response.constant('response')

    def post(self):
        def callback():
            from foundations_production.serving.rest_api_server_provider import get_rest_api_server

            rest_api_server = get_rest_api_server()
            model_package_mapping = rest_api_server.get_model_package_mapping()
            package_pool = rest_api_server.get_package_pool()
            user_defined_model_name = self.params['user_defined_model_name']

            model_id = model_package_mapping[user_defined_model_name]
            communicator = package_pool.get_communicator(model_id)
            communicator.set_action_request(self.params)
            predictions = communicator.get_response()
            self._raise_exception_if_available(predictions)
            return predictions

        if not self._model_package_exists():
            return Response.constant('model package not found', status=404)
        return Response('predictions', LazyResult(callback))

    def _raise_exception_if_available(self, predictions):
        if predictions.get('name'):
            raise eval(predictions['name'])
