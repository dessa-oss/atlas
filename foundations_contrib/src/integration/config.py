"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Katherine Bancroft <k.bancroft@dessa.com>, 06 2018
"""


# separates test runs
from uuid import uuid4
from os import getcwd, environ

if 'TEST_UUID' not in environ:
    environ['TEST_UUID'] = str(uuid4())
    environ['ARCHIVE_ROOT'] = getcwd() + '/tmp/archives_{}/archive'.format(environ['TEST_UUID'])

TEST_UUID = environ['TEST_UUID']
ARCHIVE_ROOT = environ['ARCHIVE_ROOT']

def _config():
    from foundations_contrib.global_state import config_manager
    from foundations import config_manager, LocalFileSystemPipelineArchive, LocalFileSystemPipelineListing, LocalFileSystemCacheBackend
    
    config_manager['job_notification_channel'] = 'spamity'
    config_manager['job_notification_channel_id'] = 'CM6U16G4D'

    # below is used to create archives for all different types

    archive_implementation = {
        'archive_type': LocalFileSystemPipelineArchive,
        'constructor_arguments': [ARCHIVE_ROOT],
    }
    config_manager['archive_listing_implementation'] = {
        'archive_listing_type': LocalFileSystemPipelineListing,
        'constructor_arguments': [ARCHIVE_ROOT],
    }
    config_manager['stage_log_archive_implementation'] = archive_implementation
    config_manager['persisted_data_archive_implementation'] = archive_implementation
    config_manager['provenance_archive_implementation'] = archive_implementation
    config_manager['job_source_archive_implementation'] = archive_implementation
    config_manager['artifact_archive_implementation'] = archive_implementation
    config_manager['miscellaneous_archive_implementation'] = archive_implementation
    config_manager['artifact_path'] = 'results'
    config_manager['log_level'] = 'CRITICAL'
    config_manager['obfuscate_foundations'] = False


_config()