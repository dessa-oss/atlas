"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class IntegrationConfig(object):
    def __init__(self):
        from uuid import uuid4
        from os import getcwd

        test_uuid = uuid4()

        self._cache_root = '/tmp/foundations_example_{}'.format(test_uuid)
        self._current_run_archive = getcwd() + '/tmp/archives_{}'.format(test_uuid)

    def config(self):
        from foundations import config_manager, LocalFileSystemCacheBackend, LocalFileSystemPipelineArchive, LocalFileSystemPipelineListing

        # below is used to ensure we get a different cache for every run
        config_manager['cache_implementation'] = {
            'cache_type': LocalFileSystemCacheBackend,
            'constructor_arguments': [self._cache_root],
        }

        # below is used to create archives for all different types
        archive_implementation = {
            'archive_type': LocalFileSystemPipelineArchive,
            'constructor_arguments': [self._current_run_archive],
        }
        config_manager['archive_listing_implementation'] = {
            'archive_listing_type': LocalFileSystemPipelineListing,
            'constructor_arguments': [self._current_run_archive],
        }
        config_manager['stage_log_archive_implementation'] = archive_implementation
        config_manager['persisted_data_archive_implementation'] = archive_implementation
        config_manager['provenance_archive_implementation'] = archive_implementation
        config_manager['job_source_archive_implementation'] = archive_implementation
        config_manager['artifact_archive_implementation'] = archive_implementation
        config_manager['miscellaneous_archive_implementation'] = archive_implementation

    def cleanup(self):
        from os import mkdir
        from shutil import rmtree

        rmtree(self._current_run_archive)
        mkdir(self._current_run_archive)

integration_config = IntegrationConfig()
integration_config.config()