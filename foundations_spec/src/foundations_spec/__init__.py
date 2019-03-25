"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec.helpers import *
from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers.conditional_return import ConditionalReturn
from foundations_spec.helpers.partial_callable_mock import PartialCallableMock

def _append_module():
    import sys
    from foundations_internal.global_state import module_manager

    module_manager.append_module(sys.modules[__name__])


_append_module()
