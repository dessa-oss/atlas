"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def update_default_model_for_project(ingress_resource_yaml, project_name, default_model):
    import yaml

    new_ingress = dict(ingress_resource_yaml)
    new_endpoint = {'path': f'/{project_name}', 'backend': {'serviceName': f'{project_name}-{default_model}-service', 'servicePort': 80}}
    new_paths = new_ingress['spec']['rules'][0]['http']['paths']
    new_paths = new_paths if new_paths else []

    for project in new_paths:
        if project['path'] == f'/{project_name}':
            project['backend']['serviceName'] = f'{project_name}-{default_model}-service'
            break
    else:
        new_paths.append(new_endpoint)

    new_ingress['spec']['rules'][0]['http']['paths'] = new_paths
    return new_ingress
