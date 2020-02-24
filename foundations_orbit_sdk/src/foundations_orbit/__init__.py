
from foundations_orbit.production_metrics import track_production_metrics
from foundations_orbit.data_contract import DataContract

def _append_module():
    import sys
    from foundations_internal.global_state import module_manager

    module_manager.append_module(sys.modules[__name__])

_append_module()
