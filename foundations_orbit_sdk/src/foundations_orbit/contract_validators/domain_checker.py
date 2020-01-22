"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 01 2020
"""


class DomainChecker:
    def __init__(self):
        self._unique_values = None

    def validate(self, dataframe_to_validate):
        summary = {
            'healthy': 0,
            'critical': 0,
            'warning': 0
        }
        details_by_attribute = []

        for column in dataframe_to_validate.columns:
            detail = { 'attribute_name': column }
            in_domain_mask = dataframe_to_validate[column].isin(self._unique_values[column])
            column_test_passed = in_domain_mask.all()

            if column_test_passed:
                summary['healthy'] += 1
                detail['validation_outcome'] = 'healthy'
            else:
                summary['critical'] += 1
                detail['validation_outcome'] = 'critical'
                detail['values_out_of_bounds'] = list(dataframe_to_validate[column].mask(in_domain_mask).dropna().unique())
                detail['percentage_out_of_bounds'] = (~in_domain_mask).sum() / len(in_domain_mask)

            details_by_attribute.append(detail)

        return {
            'summary': summary,
            'details_by_attribute': details_by_attribute
        }

    def calculate_stats_from_dataframe(self, reference_dataframe):
        import pandas as pd

        self._unique_values = reference_dataframe.apply(pd.unique)

    def configure(self, attributes=[]):
        pass