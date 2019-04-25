"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

def preprocessor(preprocessor_callback):
    from foundations_production.preprocessor_class import Preprocessor
    return Preprocessor(preprocessor_callback, "transformer")

def model(preprocessor_callback):
    from foundations_production.preprocessor_class import Preprocessor
    return Preprocessor(preprocessor_callback, "model")

def _append_module():
    import sys
    from foundations_contrib.global_state import module_manager

    module_manager.append_module(sys.modules[__name__])

_append_module()
model_package = None