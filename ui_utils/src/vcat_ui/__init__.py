"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat_ui.installer import _install
from mlflow import start_run


def _append_module():
    import sys
    from vcat.global_state import module_manager
    module_manager.append_module(sys.modules[__name__])


_append_module()
_install()
