"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import subprocess as sp

from flask_restful import reqparse, inputs

from foundations_rest_api.utils.api_resource import api_resource
from foundations_core_rest_api_components.response import Response
from foundations_core_rest_api_components.lazy_result import LazyResult

@api_resource('/api/v2beta/upload_to_tensorboard')
class TensorboardController:

    def post(self):
        import requests
        
        response = requests.post(f'{self._tensorboard_api_host()}/create_sym_links', json=self.params)
        if response.status_code == 400:
            return Response('Bad Request', LazyResult(lambda: response.text), status=400)
        elif response.status_code == 500:
            return Response('Tensorboard Rest API Error', LazyResult(lambda: 'Internal Server Error', status=500)) 
        return Response('Jobs', LazyResult(lambda: {'url': f'{self._tensorboard_host()}'}))

    @staticmethod
    def _tensorboard_api_host():
        from foundations_contrib.global_state import config_manager
        return config_manager['TENSORBOARD_API_HOST']

    @staticmethod
    def _tensorboard_host():
        from foundations_contrib.global_state import config_manager
        return config_manager['TENSORBOARD_HOST']
