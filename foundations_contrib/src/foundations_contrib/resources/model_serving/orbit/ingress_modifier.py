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

def add_new_model_to_ingress(project_name, model_name):
    import os

    ingress_resource = yaml.load(_run_command('kubectl get ingress model-service-selection -n ingress-nginx-test -o yaml'.split()).stdout)

    modified_ingress_resource = ingress.set_model_endpoint(ingress_resource, project_name, model_name)

    with open('temp.yaml', 'w') as yaml_file:
        yaml.dump(modified_ingress_resource, yaml_file)

    _run_command(f'kubectl apply -f temp.yaml')

    os.remove('temp.yaml')

def _run_command(command: List[str], cwd: str=None) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=True, cwd=cwd)
    except subprocess.TimeoutExpired as error:
        print('Command timed out.')
        print(error.stdout.decode())
        raise Exception(error.stderr.decode())
    except subprocess.CalledProcessError as error:
        print(f'Command failed: \n\t{" ".join(command)}\n')
        raise Exception(error.stderr.decode())
    return result

if __name__ == '__main__':
    add_new_model_to_ingress(sys.argv[1], sys.argv[2])