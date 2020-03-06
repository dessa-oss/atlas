
def _inject_config_translate():
    from foundations_internal.global_state import config_translator
    import foundations_local_docker_scheduler_plugin.config.foundations_local_docker_scheduler_config_translate as translator

    config_translator.add_translator('local_docker_scheduler_plugin', translator)

def _append_module():
    import sys
    from foundations_internal.global_state import module_manager
    
    module_manager.append_module(sys.modules[__name__])

def root():
    from pathlib import Path
    return Path(__file__).parents[0]

_append_module()
_inject_config_translate()