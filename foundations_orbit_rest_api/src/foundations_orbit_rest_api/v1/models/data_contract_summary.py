"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DataContractSummary(object):

    @staticmethod
    def get(project_name, monitor_name, contract_name, date, attribute):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: DataContractSummary._get_internal(project_name, monitor_name, contract_name, date, attribute))

    @staticmethod
    def _get_internal(project_name, monitor_name, contract_name, date, attribute):
        import pickle
        from foundations_contrib.global_state import redis_connection

        redis_key = f'projects:{project_name}:monitors:{monitor_name}:validation:{contract_name}:summary'

        summary_pickle = redis_connection.hget(redis_key, str(date))

        if summary_pickle is None:
            return None

        summary = pickle.loads(summary_pickle)
        if 'attribute_summaries' not in summary or attribute not in summary['attribute_summaries']:
            return None

        return summary['attribute_summaries'][attribute]
