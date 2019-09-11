"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_core_rest_api_components.common.models.property_model import PropertyModel

class ValidationReportListing(PropertyModel):
    
    inference_period = PropertyModel.define_property()
    model_package = PropertyModel.define_property()
    data_contract = PropertyModel.define_property()

    @staticmethod
    def all(project_name):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: ValidationReportListing._all_internal(project_name))

    @staticmethod
    def _all_internal(project_name):
        keys = ValidationReportListing._all_keys(project_name)

        if not keys:
            return []

        model_package, data_contract, inference_period = ValidationReportListing._parsed_information(keys)
        return [ValidationReportListing(model_package=model_package, data_contract=data_contract, inference_period=inference_period)]

    @staticmethod
    def _all_keys(project_name):
        from foundations_contrib.global_state import redis_connection
        return redis_connection.keys(f'projects:{project_name}:models:*:validation*')

    @staticmethod
    def _parsed_information(keys):
        from foundations_contrib.global_state import redis_connection

        key = keys[0]
        date = redis_connection.hkeys(key)[0]
        key_information = key.decode().split(':')
        return key_information[3], key_information[5], date.decode()