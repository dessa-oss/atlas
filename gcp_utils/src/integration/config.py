"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from uuid import uuid4

# separates test runs
TEST_UUID = uuid4()


def code_path():
    return 'foundations-code-test'


def result_path():
    return 'foundations-result-test'


def _config():
    from vcat import config_manager
    from vcat_gcp import GCPPipelineArchive, GCPPipelineArchiveListing

    # archive implementations
    archive_implementation = {
        'archive_type': GCPPipelineArchive,
        'constructor_arguments': [result_path()],
    }
    config_manager['archive_listing_implementation'] = {
        'archive_listing_type': GCPPipelineArchiveListing,
        'constructor_arguments': [result_path()],
    }
    config_manager['stage_log_archive_implementation'] = archive_implementation
    config_manager['persisted_data_archive_implementation'] = archive_implementation
    config_manager['provenance_archive_implementation'] = archive_implementation
    config_manager['job_source_archive_implementation'] = archive_implementation
    config_manager['artifact_archive_implementation'] = archive_implementation
    config_manager['miscellaneous_archive_implementation'] = archive_implementation

    # quiet logs
    config_manager['log_level'] = 'ERROR'


_config()
