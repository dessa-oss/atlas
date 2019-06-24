"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

# separates test runs
from uuid import uuid4
TEST_UUID = uuid4()


def _config():
    from foundations import config_manager, LocalFileSystemPipelineArchive, LocalFileSystemPipelineListing
    from foundations_scheduler_plugin.job_deployment import JobDeployment
    from foundations_spec.extensions import get_network_address
    import foundations_ssh
    import getpass
    from os import getcwd, environ

    if config_manager.frozen():
        return

    archive_implementation = {
        'archive_type': LocalFileSystemPipelineArchive,
        'constructor_arguments': ['/archive']
    }
    config_manager['archive_listing_implementation'] = {
        'archive_listing_type': LocalFileSystemPipelineListing,
        'constructor_arguments': ['/archive']
    }
    config_manager['stage_log_archive_implementation'] = archive_implementation
    config_manager['persisted_data_archive_implementation'] = archive_implementation
    config_manager['provenance_archive_implementation'] = archive_implementation
    config_manager['job_source_archive_implementation'] = archive_implementation
    config_manager['artifact_archive_implementation'] = archive_implementation
    config_manager['miscellaneous_archive_implementation'] = archive_implementation
    config_manager['log_level'] = 'CRITICAL'
    config_manager['artifact_path'] = 'results'
    config_manager['obfuscate_foundations'] = False
    config_manager['deployment_implementation'] = { 'deployment_type': JobDeployment }
    config_manager['run_script_environment'] = {'offline_mode': 'ONLINE', 'enable_stages': True}

    config_manager['remote_user'] = 'job-uploader'
    config_manager['port'] = 31222
    config_manager['code_path'] = '/jobs'
    config_manager['key_path'] = '~/.ssh/id_foundations_scheduler'


    scheduler_host = environ.get('FOUNDATIONS_SCHEDULER_HOST', None)

    if scheduler_host is None:
        print("Please set the FOUNDATIONS_SCHEDULER_HOST environment variable to your LAN ip!")
        exit(1)

    redis_url = environ.get('FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_URL', 'redis://{}:6379'.format(scheduler_host))

    config_manager['remote_host'] = scheduler_host
    config_manager['shell_command'] = '/bin/bash'
    config_manager['redis_url'] =  redis_url

    if environ.get('RUNNING_ON_CI', 'FALSE') == 'TRUE':
        config_manager['result_path'] = '/scheduler_root/results'
    else:
        config_manager['result_path'] = '/tmp/foundations/results'

def _append_spec_module():
    import sys
    from foundations_internal.global_state import module_manager

    module_manager.append_module(sys.modules['foundations_spec'])


_config()
_append_spec_module()
