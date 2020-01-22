"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 01 2020
"""


class DomainChecker:
    def validate(self, dataframe_to_validate):
        if len(dataframe_to_validate) != 0:
            return {dataframe_to_validate.columns[0]: {'status': 'passed'}}
        return {}

    def calculate_stats_from_dataframe(self, reference_dataframe):
        pass

    def configure(self, attributes=[]):
        pass