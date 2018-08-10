"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
This file contains the configurations used by Foundations to define, for example,
where to deploy a job and store its results.  Feel free to have a look at this file,
but know that a machine learning engineer will never need to create one.  That
responsability falls to a user who wishes to create or configure an integration
with an execution environment (e.g. GCP, remote machine) or remote storage (e.g.
S3, GS) on a machine learning engineer's behalf.

Usually, this information will be provided for the machine learning engineer by
the installer / integrator of Foundations in the form of a configuration yaml.
Foundations will automatically parse that yaml prior to and during job deployment.
Defining the configuration programmatically as done here is almost always unnecessary -
it's just done for convenience here.
"""

from foundations import config_manager, LocalFileSystemCacheBackend, LocalFileSystemPipelineListing, LocalFileSystemPipelineArchive
from uuid import uuid4
from os import getcwd

# define where the cache for the execution environment
# specify what type of storage as well as where it exists relative to the execution environment
config_manager['cache_implementation'] = {
    'cache_type': LocalFileSystemCacheBackend,
    'constructor_arguments': ['/tmp/foundations_example_' + str(uuid4())],
}

# configure all archives (explained below) to store data at /tmp/archives
archive_root = '/tmp/archives'

# define how to store information generated during the execution of a job
# specify what type of storage as well as where it exists relative to the execution environment
archive_implementation = {
    'archive_type': LocalFileSystemPipelineArchive,
    'constructor_arguments': [archive_root],
}

# tied to the above - we also need to specify how to list and enumerate items within the above storage
# specify the type of enumeration method / storage as well as where it exists relative to the execution environment
config_manager['archive_listing_implementation'] = {
    'archive_listing_type': LocalFileSystemPipelineListing,
    'constructor_arguments': [archive_root],
}

# specify that the stage log, persisted data, provenance, job source, artifacts, and misc data are to be stored using archive_implementation
# (local filesystem storage at /tmp/archives in the execution environment)
config_manager['stage_log_archive_implementation'] = archive_implementation
config_manager['persisted_data_archive_implementation'] = archive_implementation
config_manager['provenance_archive_implementation'] = archive_implementation
config_manager['job_source_archive_implementation'] = archive_implementation
config_manager['artifact_archive_implementation'] = archive_implementation
config_manager['miscellaneous_archive_implementation'] = archive_implementation
