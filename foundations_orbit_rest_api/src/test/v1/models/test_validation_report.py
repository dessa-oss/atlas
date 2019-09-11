"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.models.validation_report import ValidationReport
from foundations_orbit_rest_api.v1.models.validation_report_listing import ValidationReportListing

class TestValidationReport(Spec):
    
    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def model_package(self):
        return self.faker.word()

    @let
    def data_contract(self):
        return self.faker.word()

    @let
    def inference_period(self):
        return self.faker.date()

    @set_up
    def set_up(self):
        self.redis_connection.flushall()

    def test_validation_report_get_returns_none_if_report_not_in_redis(self):
        listing_object = ValidationReportListing(inference_period=self.inference_period, model_package=self.model_package, data_contract=self.data_contract)
        promise = ValidationReport.get(project_name=self.project_name, listing_object=listing_object)
        self.assertIsNone(promise.evaluate())

    