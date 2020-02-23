

def _append_module():
    import sys
    from foundations_internal.global_state import module_manager
    
    module_manager.append_module(sys.modules[__name__])

def root():
    from pathlib import Path
    return Path(__file__).parents[0]

_append_module()