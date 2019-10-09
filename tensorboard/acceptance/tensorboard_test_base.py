"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Austin Mackillop, 08 2019
"""

from foundations_spec import *
from .mixins.kubernetes_api_wrapper import KubernetesApiWrapper
from foundations_scheduler_deployment.deploy_tensorboard_server import deploy, deployment_yaml
from subprocess import PIPE

class TensorboardTestBase(Spec):

    @set_up
    def set_up(self):
        command = f'kubectl delete -f {deployment_yaml()} 1>/dev/null 2>&1 ; true'
        self.kubernetes_api_wrapper.run_process(command, shell=True, check=True)
        self._wait_for_termination('tensorboard', 30)
        self._create_images()
        self._deploy()

    def _deploy(self):
        deploy(self.kubernetes_api_wrapper)
        self._wait_for_deployment_to_be_available('tensorboard', 30)

    @let
    def tag(self):
        return self.faker.word()

    @let
    def pod_name(self):
        command = f'kubectl get pods -n {self._namespace} | grep tensorboard | awk \'{{print $1}}\''
        return self.kubernetes_api_wrapper.run_process(command, shell=True, check=True, stdout=PIPE).stdout.decode().strip()
        
    def _create_images(self):
        """Use bash script"""

    def _wait_for_deployment_to_be_available(self, grep, timeout):
        # Greps the available pods number, should be 1 on success in this case. Should make generic.
        check_availability = f'kubectl get deployments -n {self._namespace} | grep {grep} | awk \'{{print $5}}\''
        deployment_available = lambda: self.kubernetes_api_wrapper.run_process(
            check_availability, 
            shell=True, 
            check=True,
            stdout=PIPE).stdout.strip() == b'1'
        _wait_for_condition(deployment_available, timeout)    

    def _wait_for_termination(self, grep, timeout):
        deployment_does_not_exist = lambda: self.kubernetes_api_wrapper.run_process(
            f'kubectl get pods -n {self._namespace} | grep {grep}',
            shell=True,
            stdout=PIPE).stdout == ''
        _wait_for_condition(deployment_does_not_exist, timeout)
    
        
def _wait_for_condition(condition, timeout):
    import time
    timer = 0
    while not condition() and timer < timeout:
        time.sleep(0.5)
        timer += 0.5

    if timer > timeout:
        raise TimeoutError
