from vcat_gcp.gcp_job_deployment import GCPJobDeployment
from vcat_gcp.gcp_pipeline_archive import GCPPipelineArchive
from vcat_gcp.gcp_pipeline_archive_listing import GCPPipelineArchiveListing
from vcat_gcp.gcp_cache_backend import GCPCacheBackend
from vcat_gcp.gcp_bucket import GCPBucket
from vcat_gcp.global_state import *

def _append_module():
    import sys
    from vcat.global_state import module_manager
    module_manager.append_module(sys.modules[__name__])

_append_module()
