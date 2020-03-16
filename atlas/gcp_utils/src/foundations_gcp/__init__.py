
from foundations_gcp.gcp_pipeline_archive import GCPPipelineArchive
from foundations_gcp.gcp_pipeline_archive_listing import GCPPipelineArchiveListing
from foundations_gcp.gcp_bucket import GCPBucket
from foundations_gcp.global_state import *
from foundations_gcp.versioning import __version__


def _append_module():
    import sys
    from foundations_internal.global_state import module_manager
    module_manager.append_module(sys.modules[__name__])


_append_module()


