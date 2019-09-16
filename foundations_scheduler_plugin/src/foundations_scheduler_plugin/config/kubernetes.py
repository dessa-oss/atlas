"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def kubernetes_master_ip():
    import subprocess
    import yaml
    from urllib.parse import urlparse

    config_yaml = subprocess.check_output(['kubectl', 'config', 'view'])
    config = yaml.load(config_yaml)
    current_context = config['current-context']
    cluster_name = [item for item in config['contexts'] if item['name'] == current_context][0]['context']['cluster']
    cluster_server = [item for item in config['clusters'] if item['name'] == cluster_name][0]['cluster']['server']
    return urlparse(cluster_server).hostname

def kubernetes_redis_url():
    import subprocess
    import yaml
    import os

    address = "foundations-redis"
    port = "6379"

    if os.path.exists("/root/.kube"):
        endpoint_yaml = subprocess.check_output(['kubectl', 'get', 'endpoints', '-n', 'foundations-scheduler-test', 'redis', '-o', 'yaml'])
        endpoint = yaml.load(endpoint_yaml)
        subset = endpoint['subsets'][0]
        address = subset['addresses'][0]['ip']
        port = subset['ports'][0]['port']

    return f'redis://{address}:{port}'

