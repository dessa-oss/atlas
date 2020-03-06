
from foundations_ssh.versioning import __version__


def _append_module():
    import sys
    from foundations_internal import global_state
    
    global_state.module_manager.append_module(sys.modules[__name__])


_append_module()

