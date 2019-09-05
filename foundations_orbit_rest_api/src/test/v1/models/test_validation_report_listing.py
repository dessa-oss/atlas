"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.models.validation_report_listing import ValidationReportListing

class TestValidationReportListing(Spec):
    
    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def model_name(self):
        return self.faker.word()

    @let
    def data_contract_name(self):
        return self.faker.word()

    @let
    def inference_period(self):
        return self.faker.date()

    @let
    def key_to_write(self):
        return f'projects:{self.project_name}:models:{self.model_name}:validation:{self.data_contract_name}'

    @set_up
    def set_up(self):
        self.redis_connection.flushall()

    def test_validation_report_listing_get_all_returns_empty_list_for_empty_redis(self):
        promise = ValidationReportListing.all(project_name=self.project_name)
        self.assertEqual([], promise.evaluate())