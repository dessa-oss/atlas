"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.hyperparameter import Hyperparameter
from foundations.job import Job
from foundations.job_source_bundle import JobSourceBundle
from foundations.local_shell_job_deployment import LocalShellJobDeployment
from foundations.pipeline_context import PipelineContext
from foundations.pipeline import Pipeline
from foundations.result_reader import ResultReader
from foundations.stage_context import StageContext
from foundations.job_source_bundle import JobSourceBundle
from foundations.local_bundled_pipeline_archive import LocalBundledPipelineArchive
from foundations.pipeline_archiver import PipelineArchiver
from foundations.context_aware import context_aware
from foundations.pipeline_archiver_fetch import PipelineArchiverFetch
from foundations.null_cache_backend import NullCacheBackend
from foundations.local_file_system_cache_backend import LocalFileSystemCacheBackend
from foundations.global_state import *
from foundations.deployment_utils import *
from foundations.job_persister import JobPersister
from foundations.null_archive import NullArchive
from foundations.null_pipeline_archive_listing import NullArchiveListing
from foundations.local_file_system_pipeline_archive import LocalFileSystemPipelineArchive
from foundations.local_file_system_bucket import LocalFileSystemBucket
from foundations.simple_worker import SimpleWorker
from foundations.simple_bucket_worker import SimpleBucketWorker
from foundations.compat import compat_raise
from foundations.local_file_system_pipeline_listing import LocalFileSystemPipelineListing
from foundations.bucket_pipeline_archive import BucketPipelineArchive
from foundations.bucket_pipeline_listing import BucketPipelineListing
from foundations.simple_tempfile import SimpleTempfile
from foundations.prefixed_bucket import PrefixedBucket
from foundations.cached_pipeline_archive import CachedPipelineArchive
from foundations.serializer import *
from foundations.discrete_hyperparameter import DiscreteHyperparameter
from foundations.integer_hyperparameter import IntegerHyperparameter
from foundations.floating_hyperparameter import FloatingHyperparameter
from foundations.basic_stage_middleware import BasicStageMiddleware
from foundations.change_directory import ChangeDirectory
from foundations.bucket_job_deployment import BucketJobDeployment
from foundations.deployment_wrapper import DeploymentWrapper
from foundations.stage_logging import log_metric
from foundations.staging import create_stage
from foundations.projects import set_project_name
from foundations.scheduler import Scheduler
from foundations.versioning import __version__

import foundations.import_installer

def _append_module():
    import sys
    module_manager.append_module(sys.modules[__name__])

_append_module()
