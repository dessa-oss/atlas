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

