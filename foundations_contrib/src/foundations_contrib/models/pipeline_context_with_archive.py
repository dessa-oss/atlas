"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.helpers.wrap_class_with_dependency import wrap_class_with_dependency
from foundations_internal.pipeline_context import PipelineContext


@wrap_class_with_dependency(
    PipelineContext,
    'load_stage_log_from_archive',
    'load_persisted_data_from_archive',
    'load_provenance_from_archive',
    'load_job_source_from_archive',
    'load_artifact_from_archive',
    'load_miscellaneous_from_archive',
    'load_from_archive'
)
class PipelineContextWithArchive(object):
    pass
