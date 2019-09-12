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
    def model_package(self):
        return self.faker.word()

    @let
    def data_contract(self):
        return self.faker.word()

    @let
    def inference_period(self):
        return self.faker.date()

    @let
    def model_package_2(self):
        return self.faker.word()

    @let
    def data_contract_2(self):
        return self.faker.word()

    @let
    def inference_period_2(self):
        return self.faker.date()

    @set_up
    def set_up(self):
        self.redis_connection.flushall()

    def test_validation_report_listing_has_inference_period(self):
        self._test_validation_report_listing_has_property('inference_period')

    def test_validation_report_listing_has_model_package(self):
        self._test_validation_report_listing_has_property('model_package')

    def test_validation_report_listing_has_data_contract(self):
        self._test_validation_report_listing_has_property('data_contract')

    def test_validation_report_listing_get_all_returns_empty_list_for_empty_redis(self):
        promise = ValidationReportListing.all(project_name=self.project_name)
        self.assertEqual([], promise.evaluate())

    def test_validation_report_listing_get_all_returns_singleton_when_one_report_exists_in_redis(self):
        self._register_report(self.project_name, self.model_package, self.data_contract, self.inference_period)

        promise = ValidationReportListing.all(project_name=self.project_name)

        expected_result = [
            ValidationReportListing(data_contract=self.data_contract, model_package=self.model_package, inference_period=self.inference_period)
        ]

        self.assertEqual(expected_result, promise.evaluate())

    def test_validation_report_listing_get_all_returns_empty_list_if_no_key_matching_pattern_exists_in_redis_project_prefix_wrong(self):
        key_to_write = f'bep:{self.project_name}:models:{self.model_package}:validation:{self.data_contract}'
        self.redis_connection.hset(key_to_write, 'whut', 'woop')

        promise = ValidationReportListing.all(project_name=self.project_name)

        self.assertEqual([], promise.evaluate())

    def test_validation_report_listing_get_all_returns_empty_list_if_project_name_does_not_match(self):
        key_to_write = f'projects:bad_project_name:models:{self.model_package}:validation:{self.data_contract}'
        self.redis_connection.hset(key_to_write, 'whut', 'woop')

        promise = ValidationReportListing.all(project_name=self.project_name)

        self.assertEqual([], promise.evaluate())

    def test_validation_report_listing_get_all_returns_empty_list_if_no_key_matching_pattern_exists_in_redis_models_token_wrong(self):
        key_to_write = f'projects:{self.project_name}:beetles:{self.model_package}:validation:{self.data_contract}'
        self.redis_connection.hset(key_to_write, 'whut', 'woop')

        promise = ValidationReportListing.all(project_name=self.project_name)

        self.assertEqual([], promise.evaluate())

    def test_validation_report_listing_get_all_returns_empty_list_if_no_key_matching_pattern_exists_in_redis_validation_token_wrong(self):
        key_to_write = f'projects:{self.project_name}:models:{self.model_package}:beeble:{self.data_contract}'
        self.redis_connection.hset(key_to_write, 'whut', 'woop')

        promise = ValidationReportListing.all(project_name=self.project_name)

        self.assertEqual([], promise.evaluate())

    def test_validation_report_listing_get_all_returns_empty_list_if_no_key_matching_pattern_exists_in_redis_contract_name_missing(self):
        key_to_write = f'projects:{self.project_name}:models:{self.model_package}:validation'
        self.redis_connection.hset(key_to_write, 'whut', 'woop')

        promise = ValidationReportListing.all(project_name=self.project_name)

        self.assertEqual([], promise.evaluate())

    def test_validation_report_listing_get_all_returns_all_listings_when_multiple_reports_exist_in_redis_sorted_by_inference_period(self):
        self._register_report(self.project_name, self.model_package, self.data_contract, '2019-10-13')
        self._register_report(self.project_name, self.model_package_2, self.data_contract_2, '2019-03-04')

        promise = ValidationReportListing.all(project_name=self.project_name)

        expected_result = [
            ValidationReportListing(data_contract=self.data_contract_2, model_package=self.model_package_2, inference_period='2019-03-04'),
            ValidationReportListing(data_contract=self.data_contract, model_package=self.model_package, inference_period='2019-10-13')
        ]


        self.assertEqual(expected_result, promise.evaluate())

    def test_validation_report_listing_get_all_returns_all_listings_when_multiple_reports_exist_in_redis_sorted_by_inference_period_then_by_model_package(self):
        self._register_report(self.project_name, 'dog_bark', self.data_contract_2, '2019-10-13')
        self._register_report(self.project_name, 'cat_meow', self.data_contract, '2019-10-13')

        promise = ValidationReportListing.all(project_name=self.project_name)

        expected_result = [
            ValidationReportListing(data_contract=self.data_contract, model_package='cat_meow', inference_period='2019-10-13'),
            ValidationReportListing(data_contract=self.data_contract_2, model_package='dog_bark', inference_period='2019-10-13')
        ]


        self.assertEqual(expected_result, promise.evaluate())

    def test_validation_report_listing_get_all_returns_all_listings_when_multiple_reports_exist_in_redis_sorted_by_inference_period_then_by_model_package_then_by_data_contract(self):
        self._register_report(self.project_name, 'cat_meow', 'data_contract_2', '2019-10-13')
        self._register_report(self.project_name, 'cat_meow', 'data_contract', '2019-10-13')

        promise = ValidationReportListing.all(project_name=self.project_name)

        expected_result = [
            ValidationReportListing(data_contract='data_contract', model_package='cat_meow', inference_period='2019-10-13'),
            ValidationReportListing(data_contract='data_contract_2', model_package='cat_meow', inference_period='2019-10-13')
        ]


        self.assertEqual(expected_result, promise.evaluate())

    def test_validation_report_listing_get_all_returns_all_listings_when_there_is_a_single_report_and_contract_with_multiple_dates(self):
        self._register_report(self.project_name, 'cat_meow', 'data_contract', '2019-10-13')
        self._register_report(self.project_name, 'cat_meow', 'data_contract', '2019-03-04')

        promise = ValidationReportListing.all(project_name=self.project_name)

        expected_result = [
            ValidationReportListing(data_contract='data_contract', model_package='cat_meow', inference_period='2019-03-04'),
            ValidationReportListing(data_contract='data_contract', model_package='cat_meow', inference_period='2019-10-13')
        ]


        self.assertEqual(expected_result, promise.evaluate())

    def _test_validation_report_listing_has_property(self, property_name):
        property_value = getattr(self, property_name)
        kwargs = {property_name: property_value}
        listing_entry = ValidationReportListing(**kwargs)
        self.assertEqual(property_value, getattr(listing_entry, property_name))

    @staticmethod
    def _key_to_write(project_name, model_package, data_contract):
        return f'projects:{project_name}:models:{model_package}:validation:{data_contract}'

    def _register_report(self, project_name, model_package, data_contract, inference_period):
        key_to_write = self._key_to_write(project_name, model_package, data_contract)
        self.redis_connection.hset(key_to_write, inference_period, 'dummy_report')