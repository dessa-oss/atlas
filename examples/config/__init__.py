"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat import config_manager, LocalFileSystemCacheBackend, LocalFileSystemPipelineListing, LocalFileSystemPipelineArchive
from uuid import uuid4

# configure caching layer
config_manager['cache_implementation'] = {
    'cache_type': LocalFileSystemCacheBackend,
    'constructor_arguments': ['/tmp/vcat_example_' + str(uuid4())],
}

# configure all archive types to use the sample implementation
archive_implementation = {
    'archive_type': LocalFileSystemPipelineArchive,
    'constructor_arguments': ['tmp/archives'],
}
config_manager['archive_listing_implementation'] = {
    'archive_listing_type': LocalFileSystemPipelineListing,
    'constructor_arguments': ['tmp/archives'],
}
config_manager['stage_log_archive_implementation'] = archive_implementation
config_manager['persisted_data_archive_implementation'] = archive_implementation
config_manager['provenance_archive_implementation'] = archive_implementation
config_manager['job_source_archive_implementation'] = archive_implementation
config_manager['artifact_archive_implementation'] = archive_implementation
config_manager['miscellaneous_archive_implementation'] = archive_implementation