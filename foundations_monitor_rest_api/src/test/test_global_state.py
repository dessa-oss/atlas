"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 10 2019
"""

from foundations_spec import *

class TestGlobalState(Spec):

    def test_app_manager_comes_from_core_api_components(self):
        import foundations_monitor_rest_api.global_state as monitor
        import foundations_core_rest_api_components.global_state as core

        self.assertEqual(core.app_manager, monitor.app_manager)