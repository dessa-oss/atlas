"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


from os import getcwd
import shutil
from uuid import uuid4

TEST_UUID = uuid4()

integration_job_name = 'integration-job'
_local_temp_directory = getcwd() + '/tmp'

def _configure():
    import foundations
    from foundations import LocalFileSystemPipelineArchive, LocalFileSystemPipelineListing, LocalFileSystemCacheBackend
    from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
    from foundations_contrib.global_state import foundations_context
    from foundations_contrib.global_state import config_manager

    # below is used to ensure we get a different cache for every run
    config_manager['cache_implementation'] = {
        'cache_type': LocalFileSystemCacheBackend,
        'constructor_arguments': ['/tmp/foundations_example_{}'.format(TEST_UUID)],
    }

    # below is used to create archives for all different types
    archive_root = _local_temp_directory + '/archives_{}'.format(TEST_UUID)

    archive_implementation = {
        'archive_type': LocalFileSystemPipelineArchive,
        'constructor_arguments': [archive_root],
    }
    config_manager['archive_listing_implementation'] = {
        'archive_listing_type': LocalFileSystemPipelineListing,
        'constructor_arguments': [archive_root],
    }
    config_manager['deployment_implementation'] = {
        'deployment_type': LocalShellJobDeployment
    }
    config_manager['stage_log_archive_implementation'] = archive_implementation
    config_manager['persisted_data_archive_implementation'] = archive_implementation
    config_manager['provenance_archive_implementation'] = archive_implementation
    config_manager['job_source_archive_implementation'] = archive_implementation
    config_manager['artifact_archive_implementation'] = archive_implementation
    config_manager['miscellaneous_archive_implementation'] = archive_implementation
    config_manager['log_level'] = 'CRITICAL'
    config_manager['obfuscate_foundations'] = False

    foundations_context.pipeline_context().file_name = integration_job_name

shutil.rmtree(_local_temp_directory, ignore_errors=True)
_configure()