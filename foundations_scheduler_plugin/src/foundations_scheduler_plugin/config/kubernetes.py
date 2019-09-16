"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def kubernetes_master_ip():
    from urllib.parse import urlparse

    config = _run_command_and_get_yaml('kubectl config view')
    current_context = config['current-context']

    if current_context == '':
        config = _run_command_and_get_yaml('kubectl get no -o yaml -l node-role.kubernetes.io/master=')
        entries = config['items'][0]['status']['addresses']
        for entry in entries:
            if entry['type'] == 'InternalIP':
                return entry['address']
    else:
        cluster_name = [item for item in config['contexts'] if item['name'] == current_context][0]['context']['cluster']
        cluster_server = [item for item in config['clusters'] if item['name'] == cluster_name][0]['cluster']['server']
        return urlparse(cluster_server).hostname

def kubernetes_redis_url():
    import subprocess
    import yaml

    endpoint = _run_command_and_get_yaml('kubectl get endpoints -n foundations-scheduler-test redis -o yaml')
    subset = endpoint['subsets'][0]
    address = subset['addresses'][0]['ip']
    port = subset['ports'][0]['port']
    return f'redis://{address}:{port}'

def _run_command_and_get_yaml(command):
    import subprocess
    import yaml

    config_yaml = subprocess.check_output(command.split())
    return yaml.load(config_yaml)