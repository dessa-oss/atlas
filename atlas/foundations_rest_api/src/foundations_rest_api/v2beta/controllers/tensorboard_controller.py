import subprocess as sp

from flask_restful import reqparse, inputs

from foundations_rest_api.utils.api_resource import api_resource
from foundations_core_rest_api_components.response import Response
from foundations_core_rest_api_components.lazy_result import LazyResult

@api_resource('/api/v2beta/upload_to_tensorboard')
class TensorboardController:

    def post(self):
        import requests
        job_ids = self.params.get('job_ids', None)
        if job_ids is None:
            return Response('Bad Request', LazyResult(lambda: 'Expected a json object with key \'job_ids\''), status=400)
        
        tb_locations = self._transform_request(job_ids)

        response = requests.post(f'{self._tensorboard_api_host()}/create_sym_links', json=tb_locations)
        if response.status_code == 400:
            return Response('Bad Request', LazyResult(lambda: response.text), status=400)
        elif response.status_code == 500:
            return Response('Tensorboard Rest API Error', LazyResult(lambda: 'Internal Server Error'), status=500)
        return Response('Jobs', LazyResult(lambda: {'url': f'{self._tensorboard_host()}'}))
    
    @staticmethod
    def _transform_request(job_ids):
        path = 'archive/{}/synced_directories/__tensorboard__'
        tb_locations = [{'job_id': str(job_id), 'synced_directory': path.format(job_id)} 
                        for job_id in job_ids]
        return {'tensorboard_locations': tb_locations}

    @staticmethod
    def _tensorboard_api_host():
        import os
        return os.getenv('TENSORBOARD_API_HOST', 'localhost:5000')

    @staticmethod
    def _tensorboard_host():
        import os
        return os.getenv('TENSORBOARD_HOST', 'localhost:5959')