"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.controllers import ValidationReportListingsController

class TestValidationReportListingsController(Spec):

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @let
    def controller(self):
        return ValidationReportListingsController()

    @set_up
    def set_up(self):
        self.redis_connection.flushall()

    def test_validation_report_listings_controller_gives_empty_list_as_response_if_no_reports_in_redis(self):
        self.assertEqual([], self.controller.index().as_json())

    def test_index_returns_resource_with_resource_name_validation_report_listings(self):
        result = self.controller.index()
        self.assertEqual('ValidationReportListings', result.resource_name())