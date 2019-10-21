"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ValidationReport(object):
    
    @staticmethod
    def get(project_name=None, listing_object=None):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: ValidationReport._get_internal(project_name, listing_object))

    @staticmethod
    def _get_internal(project_name, listing_object):
        import pickle
        from foundations_contrib.global_state import redis_connection

        attributes = listing_object.attributes        

        inference_period = attributes['inference_period']
        monitor_package = attributes['model_package']
        data_contract = attributes['data_contract']

        redis_key = f'projects:{project_name}:monitors:{monitor_package}:validation:{data_contract}'
        
        report = redis_connection.hget(redis_key, inference_period)

        if report is None:
            return None
        return pickle.loads(report)
