"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def update_default_model_for_project(ingress_resource_yaml, project_name, default_model):
    return _add_new_path_to_ingress_resource(ingress_resource_yaml, f'{project_name}', f'{project_name}-{default_model}-service')

def set_model_endpoint(ingress_resource_yaml, project_name, model_name):
    return _add_new_path_to_ingress_resource(ingress_resource_yaml, f'{project_name}/{model_name}', f'{project_name}-{model_name}-service')

def _add_new_path_to_ingress_resource(ingress_resource_yaml, endpoint_path, service_name):
    new_ingress = ingress_resource_yaml
    new_paths = _get_paths_from_ingress_resource(new_ingress)

    _update_default_endpoint_if_exists(new_paths, endpoint_path, service_name)

    new_ingress['spec']['rules'][0]['http']['paths'] = new_paths
    return new_ingress

def _get_paths_from_ingress_resource(new_ingress):
    new_paths = new_ingress['spec']['rules'][0]['http']['paths']
    new_paths = new_paths if new_paths else []

    return new_paths

def _update_default_endpoint_if_exists(new_paths, endpoint_path, service_name):

    for project in new_paths:
        if project['path'] == f'/{endpoint_path}':
            project['backend']['serviceName'] = f'{service_name}'
            break
    else:
        new_endpoint = {'path': f'/{endpoint_path}', 'backend': {'serviceName': f'{service_name}', 'servicePort': 80}}
        new_paths.append(new_endpoint)
    
    return new_paths