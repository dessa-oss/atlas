"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Katherine Bancroft <k.bancroft@dessa.com>, 06 2018
"""

import subprocess
from typing import List
import os
import time

from foundations_spec import *
from foundations_contrib.cli import model_package_server
import foundations_contrib
class TestOrbitIngress(Spec):
    
    @set_up_class
    def set_up(self):
        _run_command(['./integration/resources/fixtures/test_server/spin_up.sh'])
    
    @tear_down_class
    def tear_down(self):
        command = 'bash ./remove_deployment.sh project model'
        _run_command(command.split(), foundations_contrib.root() / 'resources/model_serving/orbit')
        _run_command(['./integration/resources/fixtures/test_server/tear_down.sh'])

    def test_first_served_model_can_be_reached_through_ingress(self):
        scheduler_host = os.environ.get('FOUNDATIONS_SCHEDULER_HOST', 'localhost')

        _run_command('./integration/resources/fixtures/test_server/setup_test_server.sh project model'.split())

        time.sleep(10)

        try:
            result = _run_command(f'curl http://{scheduler_host}:31998/project/model'.split()).stdout.decode()
        except Exception as e:
            if 'Failed to connect' in str(e):
                result = 'Failed to connect'
            else:
                raise e
        self.assertEqual('Test Passed', result)

        try:
            result = _run_command(f'curl http://{scheduler_host}:31998/project'.split()).stdout.decode()
        except Exception as e:
            if 'Failed to connect' in str(e):
                result = 'Failed to connect'
            else:
                raise e
        self.assertEqual('Test Passed', result)

    def test_second_served_model_can_be_accessed(self):
        scheduler_host = os.environ.get('FOUNDATIONS_SCHEDULER_HOST', 'localhost')

        _run_command('./integration/resources/fixtures/test_server/setup_test_server.sh project model-two'.split())

        time.sleep(10)

        try:
            result = _run_command(f'curl http://{scheduler_host}:31998/project/model-two'.split()).stdout.decode()
        except Exception as e:
            if 'Failed to connect' in str(e):
                result = 'Failed to connect'
            else:
                raise e
        self.assertEqual('Test Passed', result)

def _run_command(command: List[str], cwd: str=None) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=True, cwd=cwd)
    except subprocess.TimeoutExpired as error:
        print('Command timed out.')
        print(error.stdout.decode())
        raise Exception(error.stderr.decode())
    except subprocess.CalledProcessError as error:
        print(f'Command failed: \n\t{" ".join(command)}\n')
        raise Exception(error.stderr.decode())
    return result
