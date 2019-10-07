"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Austin Mackillop, 08 2019
"""

def deploy(kubernetes_api_wrapper):
    command = f'kubectl apply -f {deployment_yaml()}'
    kubernetes_api_wrapper.run_process(command, shell=True, check=True)

def deployment_yaml():
    from foundations_scheduler_deployment import root
    return f'{root()}/resources/kubernetes_resources/tensorboard_deployment.yaml'