"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

# separates test runs
from uuid import uuid4
TEST_UUID = uuid4()


def set_foundations_home():
    import os

    os.environ['FOUNDATIONS_HOME'] = os.getcwd() + '/foundations_home'
    os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'

def _config():
    from foundations_contrib.global_state import config_manager, foundations_context, redis_connection
    from foundations_contrib.cli.typed_config_listing import TypedConfigListing
    from foundations_scheduler_plugin.config.scheduler import translate
    from foundations_scheduler_plugin.job_deployment import JobDeployment
    from foundations_scheduler_plugin.config.kubernetes import kubernetes_master_ip
    from foundations_spec.extensions import get_network_address
    from foundations_internal.job_resources import JobResources
    import foundations_ssh
    import getpass
    from os import getcwd, environ

    foundations_context.set_job_resources(JobResources(0, None))

    if config_manager.frozen():
        return

    TypedConfigListing('submission').update_config_manager_with_config('scheduler', translate)

    config = config_manager.config()
    config['run_script_environment'] = {'offline_mode': 'ONLINE', 'enable_stages': True}
    scheduler_host = config['remote_host']

    redis_url = environ.get('FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_URL', 'redis://{}:6379'.format(scheduler_host))
    config['redis_url'] =  redis_url

    _set_tensorboard_hosts(config, scheduler_host)

def _set_tensorboard_hosts(config, scheduler_host):
    tensorboard_host = f'http://{scheduler_host}'
    config['TENSORBOARD_API_HOST'] = f'{tensorboard_host}:32767'
    config['TENSORBOARD_HOST'] = f'{tensorboard_host}:32766'

def _append_spec_module():
    import sys
    from foundations_internal.global_state import module_manager

    module_manager.append_module(sys.modules['foundations_spec'])

set_foundations_home()
_config()
_append_spec_module()
