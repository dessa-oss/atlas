"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_gcp.gcp_pipeline_archive import GCPPipelineArchive
from foundations_gcp.gcp_pipeline_archive_listing import GCPPipelineArchiveListing
from foundations_gcp.gcp_cache_backend import GCPCacheBackend
from foundations_gcp.gcp_bucket import GCPBucket
from foundations_gcp.global_state import *
from foundations_gcp.versioning import __version__


def _append_module():
    import sys
    from foundations_internal.global_state import module_manager
    module_manager.append_module(sys.modules[__name__])


_append_module()


