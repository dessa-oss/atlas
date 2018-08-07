"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
This file contains the configurations used by Foundations to define, for example,
where to deploy a job and store its results.  Feel free to have a look at this file,
but know that you'll never need to create one youself.
"""

from foundations import config_manager, LocalFileSystemCacheBackend, LocalFileSystemPipelineListing, LocalFileSystemPipelineArchive
from uuid import uuid4
from os import getcwd

# configure caching layer
config_manager['cache_implementation'] = {
    'cache_type': LocalFileSystemCacheBackend,
    'constructor_arguments': ['/tmp/vcat_example_' + str(uuid4())],
}

# configure all archive types to use the sample implementation
archive_root = getcwd() + '/tmp/archives'

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
