"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestTrackProductionMetrics(Spec):

    def test_can_track_production_metrics(self):
        import foundations
        import foundations_orbit

        self.assertEqual(foundations.track_production_metrics, foundations_orbit.track_production_metrics)