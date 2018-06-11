from vcat_gcp.gcp_job_deployment import GCPJobDeployment
from vcat_gcp.gcp_pipeline_archive import GCPPipelineArchive
from vcat_gcp.gcp_pipeline_archive_listing import GCPPipelineArchiveListing
from vcat_gcp.gcp_cache_backend import GCPCacheBackend

def _append_module():
    import sys
    from vcat.global_state import module_manager
    module_manager.append_module(sys.modules[__name__])

_append_module()
