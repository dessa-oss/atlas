
import foundations_contrib.config
import foundations_contrib._promise_hacks


def root():
    from pathlib import Path
    return Path(__file__).parents[0]


def _append_module():
    import sys
    from foundations_internal.global_state import module_manager

    module_manager.append_module(sys.modules[__name__])


def hide_yaml_warnings_for_deprecated_version():
    import warnings
    from yaml import YAMLLoadWarning
    warnings.filterwarnings('ignore', category=YAMLLoadWarning)


hide_yaml_warnings_for_deprecated_version()
_append_module()