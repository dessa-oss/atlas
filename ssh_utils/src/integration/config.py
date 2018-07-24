"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from uuid import uuid4

# for running jobs remotely
DEPLOYMENT_CONFIG = {}

# separates test runs
TEST_UUID = uuid4()


def code_path():
    from os import getcwd
    return '{}/tmp/code_{}'.format(getcwd(), TEST_UUID)


def result_path():
    from os import getcwd
    return '{}/tmp/results_{}'.format(getcwd(), TEST_UUID)


def _config():
    from os.path import isfile, expanduser
    from getpass import getuser
    from foundations import config_manager, LocalFileSystemPipelineArchive
    from foundations_ssh import MultiSFTPBundledPipelineArchive, SFTPListing

    # read archive implementations
    archive_implementation = {
        'archive_type': MultiSFTPBundledPipelineArchive,
        'constructor_arguments': [],
    }
    config_manager['archive_listing_implementation'] = {
        'archive_listing_type': SFTPListing,
        'constructor_arguments': [],
    }
    config_manager['stage_log_archive_implementation'] = archive_implementation
    config_manager['persisted_data_archive_implementation'] = archive_implementation
    config_manager['provenance_archive_implementation'] = archive_implementation
    config_manager['job_source_archive_implementation'] = archive_implementation
    config_manager['artifact_archive_implementation'] = archive_implementation
    config_manager['miscellaneous_archive_implementation'] = archive_implementation

    # quiet logs
    config_manager['log_level'] = 'ERROR'

    # remote access config
    config_manager['remote_user'] = getuser()
    config_manager['remote_host'] = 'localhost'
    config_manager['code_path'] = code_path()
    config_manager['result_path'] = result_path()
    config_manager['shell_command'] = '/bin/bash'

    # ensure an ssh key is available
    key_path = expanduser('~/.ssh/id_local')
    if not isfile(key_path):
        raise Exception(
            'Please create a local ssh key at ~/.ssh/id_local and add the public key to ~/.ssh/authorized_keys to run integration tests')
    config_manager['key_path'] = key_path


_config()
