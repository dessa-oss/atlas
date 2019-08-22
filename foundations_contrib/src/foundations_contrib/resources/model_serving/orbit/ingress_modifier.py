"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.resources.model_serving.orbit import ingress
from typing import List
import subprocess
import yaml
import sys
import os
import json

def add_new_model_to_ingress(project_name, model_name, namespace='foundations-scheduler-test'):

    ingress_resource = yaml.load(_run_command(f'kubectl get ingress model-service-selection -n {namespace} -o yaml'.split()).stdout.decode())

    previous_configuration = ingress_resource['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration'].strip('\n')

    ingress_resource_to_modify = json.loads(previous_configuration)

    modified_ingress_resource = ingress.set_model_endpoint(ingress_resource_to_modify, project_name, model_name)

    temp_file_path = _temp_file_path()
    with open(f'{temp_file_path}', 'w') as yaml_file:
        yaml.dump(modified_ingress_resource, yaml_file, default_flow_style=False)

    _run_command(f'kubectl apply -f {temp_file_path}'.split())

    # os.remove(f'{temp_file_path}')

def _run_command(command: List[str], cwd: str=None) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=True, cwd=cwd)
    except subprocess.TimeoutExpired as error:
        raise Exception(error.stderr.decode())
    except subprocess.CalledProcessError as error:
        raise Exception(error.stderr.decode())
    return result

def _temp_file_path():
    return f'/var/tmp/{_temp_file_name()}'

def _temp_file_name():
    return f'temp-{os.getpid()}.yaml'

if __name__ == '__main__':
    add_new_model_to_ingress(sys.argv[1], sys.argv[2])