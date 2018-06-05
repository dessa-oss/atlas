from vcat_ssh.ssh_job_deployment import SSHJobDeployment
from vcat_ssh.ssh_listing import SSHListing
from vcat_ssh.multi_ssh_bundled_pipeline_archive import MultiSSHBundledPipelineArchive

def _append_module():
    import sys
    from vcat.global_state import module_manager
    module_manager.append_module(sys.modules[__name__])

_append_module()
