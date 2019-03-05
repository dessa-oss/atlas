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
    from os import getcwd, environ
    from foundations import config_manager, LocalFileSystemPipelineArchive, LocalFileSystemPipelineListing
    import foundations_ssh

    archive_implementation = {
        'archive_type': LocalFileSystemPipelineArchive
    }
    config_manager['archive_listing_implementation'] = {
        'archive_listing_type': LocalFileSystemPipelineListing
    }
    config_manager['stage_log_archive_implementation'] = archive_implementation
    config_manager['persisted_data_archive_implementation'] = archive_implementation
    config_manager['provenance_archive_implementation'] = archive_implementation
    config_manager['job_source_archive_implementation'] = archive_implementation
    config_manager['artifact_archive_implementation'] = archive_implementation
    config_manager['miscellaneous_archive_implementation'] = archive_implementation
    config_manager['log_level'] = 'CRITICAL'
    config_manager['remote_user'] = 'foundations'
    config_manager['remote_host'] = environ['FOUNDATIONS_SCHEDULER_HOST'] 
    config_manager['shell_command'] = '/bin/bash'
    config_manager['code_path'] = '/scheduler_root/jobs'
    config_manager['result_path'] = '/scheduler_root/results'
    config_manager['key_path'] = '/tmp/scheduler.pem'
    config_manager['deployment_implementation'] = {
        'deployment_type': foundations_ssh.SFTPJobDeployment
    }

_config()