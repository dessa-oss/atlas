"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

def _inject_config_translate():
    from foundations_internal.global_state import config_translator
    import foundations_scheduler_plugin.config.foundations_scheduler_config_translate as translator

    config_translator.add_translator('scheduler_plugin', translator)

def _append_module():
    import sys
    from foundations_internal.global_state import module_manager
    
    module_manager.append_module(sys.modules[__name__])

def root():
    from pathlib import Path
    return Path(__file__).parents[0]

_append_module()
_inject_config_translate()