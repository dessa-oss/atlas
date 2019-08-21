"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

from foundations_aws.aws_pipeline_archive import AWSPipelineArchive
from foundations_aws.aws_pipeline_archive_listing import AWSPipelineArchiveListing
from foundations_aws.aws_cache_backend import AWSCacheBackend
from foundations_aws.aws_bucket import AWSBucket
from foundations_aws.global_state import *


def _append_module():
    import sys
    from foundations_internal.global_state import module_manager
    module_manager.append_module(sys.modules[__name__])


_append_module()