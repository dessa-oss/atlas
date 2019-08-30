"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import subprocess as sp

from flask_restful import reqparse, inputs
import requests

from foundations_rest_api.utils.api_resource import api_resource
from foundations_core_rest_api_components.response import Response
from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_contrib.helpers.run_command import run_command

def _get_cluster_ip(namespace, service_to_grep):
    get_ip = f"kubectl get services -n {namespace} | grep {service_to_grep} | awk '{{print $3}}'"
    result = run_command(get_ip)
    return result.stdout.decode().strip()

@api_resource('/api/v2beta/upload_to_tensorboard')
class TensorboardController:

    parser = reqparse.RequestParser()
    parser.add_argument('job_ids', action='append')
    
    _cluster_ip = _get_cluster_ip('foundations-scheduler-test', 'tensorboard')

    def post(self):
        job_ids = self.parser.parse_args()
        response = requests.post(f'http://{self._cluster_ip}/create_sym_links', json=job_ids)
        return Response('Tensorboard', LazyResult(lambda: response.text))
