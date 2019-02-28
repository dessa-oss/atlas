"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Katherine Bancroft <k.bancroft@dessa.com>, 06 2018
"""

import foundations_contrib.config
import foundations_contrib._promise_hacks

def root():
    from pathlib import Path
    return Path(__file__).parents[0]


def _append_module():
    import sys
    from foundations_internal.global_state import module_manager

    module_manager.append_module(sys.modules[__name__])


_append_module()


def _inject_config_translate():
    from foundations_internal.global_state import config_translator
    import foundations_contrib.config.local_config_translate as translator

    config_translator.add_translator('local', translator)


_inject_config_translate()
