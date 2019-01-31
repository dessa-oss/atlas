"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def _inject_config_translator():
    from fondations_internal.global_state import config_translator
    import fondations_contrib.config.local_config_translate as translator
    config_translator.add_translator('local', translator)