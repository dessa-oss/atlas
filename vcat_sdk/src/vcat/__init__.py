"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.hyperparameter import Hyperparameter
from vcat.job import Job
from vcat.job_source_bundle import JobSourceBundle
from vcat.local_shell_job_deployment import LocalShellJobDeployment
from vcat.pipeline_context import PipelineContext
from vcat.pipeline import Pipeline
from vcat.result_reader import ResultReader
from vcat.stage_context import StageContext
from vcat.job_source_bundle import JobSourceBundle
from vcat.local_bundled_pipeline_archive import LocalBundledPipelineArchive
from vcat.pipeline_archiver import PipelineArchiver
from vcat.context_aware import context_aware
from vcat.pipeline_archiver_fetch import PipelineArchiverFetch
from vcat.null_cache_backend import NullCacheBackend
from vcat.local_file_system_cache_backend import LocalFileSystemCacheBackend
from vcat.global_state import *
from vcat.deployment_utils import *
from vcat.job_persister import JobPersister
from vcat.null_archive import NullArchive
from vcat.null_pipeline_archive_listing import NullArchiveListing
from vcat.local_file_system_pipeline_archive import LocalFileSystemPipelineArchive
from vcat.local_file_system_bucket import LocalFileSystemBucket
from vcat.simple_worker import SimpleWorker
from vcat.compat import compat_raise
from vcat.local_file_system_pipeline_listing import LocalFileSystemPipelineListing
from vcat.bucket_pipeline_archive import BucketPipelineArchive
from vcat.bucket_pipeline_listing import BucketPipelineListing
from vcat.simple_tempfile import SimpleTempfile
from vcat.prefixed_bucket import PrefixedBucket
from vcat.cached_pipeline_archive import CachedPipelineArchive
from vcat.serializer import *
from vcat.discrete_hyperparameter import DiscreteHyperparameter
from vcat.integer_hyperparameter import IntegerHyperparameter
from vcat.floating_hyperparameter import FloatingHyperparameter
from vcat.basic_stage_middleware import BasicStageMiddleware
from vcat.change_directory import ChangeDirectory
from vcat.bucket_job_deployment import BucketJobDeployment

import vcat.import_installer

def _append_module():
    import sys
    module_manager.append_module(sys.modules[__name__])

_append_module()
