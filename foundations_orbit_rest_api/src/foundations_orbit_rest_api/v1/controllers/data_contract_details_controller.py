"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource

@api_resource('/api/v1/contracts/<string:uuid>')
class DataContractDetailsController(object):
    
    def index(self):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_core_rest_api_components.response import Response
        from foundations_orbit_rest_api.v1.models.data_contract_details import DataContractDetails

        uuid = self.params.pop('uuid')
        response = DataContractDetails.get(uuid)

        failure_response_data = {
            'uuid': uuid,
            'error': 'UUID does not exist'
        }

        fallback = Response('asdf', LazyResult(lambda: failure_response_data), status=400)

        return Response('asdf', response, status=200, fallback=fallback)

        

