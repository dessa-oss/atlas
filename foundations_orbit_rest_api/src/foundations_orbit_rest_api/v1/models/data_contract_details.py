"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""

class DataContractDetails(object):

    @staticmethod
    def get(uuid):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: DataContractDetails._get_internal(uuid))
    
    @staticmethod
    def _get_internal(uuid):
        from foundations_contrib.global_state import redis_connection

        info_key = f'contracts:{uuid}:info'
        result = redis_connection.get(info_key)

        if result:
            result = result.decode()

        return result