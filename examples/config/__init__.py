"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
This file contains the configurations used by Foundations to define, for example,
where to deploy a job and store its results.  Feel free to have a look at this file,
but know that an MLE will never need to create one.  That responsability falls to
a user who wishes to create or configure an integration with an execution environment
(e.g. GCP, remote machine) or remote storage (e.g. S3, GS) on an MLE's behalf.
"""

from foundations import config_manager, LocalFileSystemCacheBackend, LocalFileSystemPipelineListing, LocalFileSystemPipelineArchive
from uuid import uuid4
from os import getcwd

# configure caching layer
config_manager['cache_implementation'] = {
    'cache_type': LocalFileSystemCacheBackend,
    'constructor_arguments': ['/tmp/foundations_example_' + str(uuid4())],
}

# configure all archive types to use the sample implementation
archive_root = '/tmp/archives'

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
