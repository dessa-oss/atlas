
from foundations_spec import *

class TestTrackProductionMetrics(Spec):

    @quarantine
    def test_can_track_production_metrics(self):
        import foundations
        import foundations_orbit

        self.assertEqual(foundations.track_production_metrics, foundations_orbit.track_production_metrics)