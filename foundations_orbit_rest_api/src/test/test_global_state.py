
from foundations_spec import *

class TestGlobalState(Spec):

    def test_app_manager_comes_from_core_api_components(self):
        import foundations_orbit_rest_api.global_state as orbit
        import foundations_core_rest_api_components.global_state as core

        self.assertEqual(core.app_manager, orbit.app_manager)