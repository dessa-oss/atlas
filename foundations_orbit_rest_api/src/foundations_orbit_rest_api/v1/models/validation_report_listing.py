"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_core_rest_api_components.common.models.property_model import PropertyModel

class ValidationReportListing(PropertyModel):
    
    inference_period = PropertyModel.define_property()
    monitor_package = PropertyModel.define_property()
    data_contract = PropertyModel.define_property()

    @staticmethod
    def all(project_name):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: ValidationReportListing._all_internal(project_name))

    @staticmethod
    def _all_internal(project_name):
        listing = list(ValidationReportListing._listing_stream(project_name))
        listing.sort(key=ValidationReportListing._sort_key)
        return listing

    @staticmethod
    def _sort_key(listing_entry):
        return (listing_entry.inference_period, listing_entry.monitor_package, listing_entry.data_contract)

    @staticmethod
    def _listing_stream(project_name):
        keys = ValidationReportListing._all_keys(project_name)

        for monitor_package, data_contract, inference_period in ValidationReportListing._parsed_information(keys):
            yield ValidationReportListing(monitor_package=monitor_package, data_contract=data_contract, inference_period=inference_period)

    @staticmethod
    def _all_keys(project_name):
        from foundations_contrib.global_state import redis_connection
        return redis_connection.keys(f'projects:{project_name}:monitors:*:validation:*')

    @staticmethod
    def _parsed_information(keys):
        from foundations_contrib.global_state import redis_connection

        for key in keys:
            dates = redis_connection.hkeys(key)
            for date in dates:
                key_information = key.decode().split(':')
                yield key_information[3], key_information[5], date.decode()