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
from faker import Faker

class TestOrbitIngress(Spec):
    
    namespace = 'foundations-scheduler-test'
    faker = Faker()

    model_name = faker.word()
    second_model_name = faker.word()
    project_name = faker.word()

    @let
    def sleep_time(self):
        return 60

    @set_up_class
    def set_up(self):
        _run_command(['./integration/resources/fixtures/test_server/spin_up.sh'])

    @tear_down_class
    def tear_down(self):
        command = f'bash ./remove_deployment.sh {self.project_name} {self.model_name}'
        _run_command(command.split(), foundations_contrib.root() / 'resources/model_serving/orbit')
        try:
            command = f'bash ./remove_deployment.sh {self.project_name} {self.second_model_name}'
            _run_command(command.split(), foundations_contrib.root() / 'resources/model_serving/orbit')
        except:
            print('Second test may not have created the pod')

        _run_command(['./integration/resources/fixtures/test_server/tear_down.sh', self.project_name])

    def test_first_served_model_can_be_reached_through_ingress_using_default_and_model_endpoint(self):
        _run_command(f'./integration/resources/fixtures/test_server/setup_test_server.sh {self.namespace} {self.project_name} {self.model_name}'.split())

        self._assert_endpoint_accessable(f'/projects/{self.project_name}/{self.model_name}/', 'Test Passed')
        self._assert_endpoint_accessable(f'/projects/{self.project_name}/{self.model_name}/predict', 'get on predict')
        self._assert_endpoint_accessable(f'/projects/{self.project_name}/{self.model_name}/evaluate', 'get on evaluate')

        self._assert_endpoint_accessable(f'/projects/{self.project_name}/', 'Test Passed')
        self._assert_endpoint_accessable(f'/projects/{self.project_name}/predict', 'get on predict')
        self._assert_endpoint_accessable(f'/projects/{self.project_name}/evaluate', 'get on evaluate')

    def test_second_served_model_can_be_accessed(self):
        _run_command(f'./integration/resources/fixtures/test_server/setup_test_server.sh {self.namespace} {self.project_name} {self.second_model_name}'.split())

        self._assert_endpoint_accessable(f'/projects/{self.project_name}/{self.model_name}/predict', 'get on predict')

    def _assert_endpoint_accessable(self, endpoint, expected_text):
        scheduler_host = os.environ.get('FOUNDATIONS_SCHEDULER_HOST', 'localhost')
        
        for _ in range(self.sleep_time):
            try:
                result = _run_command(f'curl http://{scheduler_host}:31998{endpoint} --connect-timeout 1'.split()).stdout.decode()
                if result:
                    self.assertEqual(expected_text, result)
                    return
            except AssertionError as ae:
                result = f'invalid result retrieved from request {ae}'
            except Exception as e:
                result = f'Failed to connect: {e}'
            time.sleep(1)
        self.fail(result)

def _run_command(command: List[str], cwd: str=None) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=True, cwd=cwd)
    except subprocess.TimeoutExpired as error:
        raise Exception(error.stderr.decode())
    except subprocess.CalledProcessError as error:
        raise Exception(error.stderr.decode())
    return result
