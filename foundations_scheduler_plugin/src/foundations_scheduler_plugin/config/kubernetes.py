"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def kubernetes_master_ip():
    import subprocess
    import yaml

    node_yaml = subprocess.check_output(['kubectl', 'get', 'node', '-o', 'yaml', '-l', 'node-role.kubernetes.io/master='])
    node = yaml.load(node_yaml)
    return node['items'][0]['status']['addresses'][0]['address']

