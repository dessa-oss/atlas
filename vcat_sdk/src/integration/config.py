"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def _config():
    from uuid import uuid4
    from os import getcwd
    from vcat import config_manager, LocalFileSystemCacheBackend, LocalFileSystemPipelineArchive, LocalFileSystemPipelineListing

    # separates test runs
    test_uuid = uuid4()

    # below is used to ensure we get a different cache for every run
    config_manager['cache_implementation'] = {
        'cache_type': LocalFileSystemCacheBackend,
        'constructor_arguments': ['/tmp/vcat_example_{}'.format(test_uuid)],
    }

    # below is used to create archives for all different types
    archive_root = getcwd() + '/tmp/archives_{}'.format(test_uuid)

    archive_implementation = {
        'archive_type': LocalFileSystemPipelineArchive,
        'constructor_arguments': [archive_root],
    }
    config_manager['archive_listing_implementation'] = {
        'archive_listing_type': LocalFileSystemPipelineListing,
        'constructor_arguments': [archive_root],
    }
    config_manager['stage_log_archive_implementation'] = archive_implementation
    config_manager['persisted_data_archive_implementation'] = archive_implementation
    config_manager['provenance_archive_implementation'] = archive_implementation
    config_manager['job_source_archive_implementation'] = archive_implementation
    config_manager['artifact_archive_implementation'] = archive_implementation
    config_manager['miscellaneous_archive_implementation'] = archive_implementation


_config()
