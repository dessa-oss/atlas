from vcat_bell.ssh_job_deployment import SSHJobDeployment

def _append_module():
    import sys
    from vcat.global_state import module_manager
    module_manager.append_module(sys.modules[__name__])

_append_module()
