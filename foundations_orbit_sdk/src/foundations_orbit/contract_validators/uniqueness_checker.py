"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Calvin Choi <c.choi@dessa.com>, 01 2020
"""

class UniquenessChecker:
    
    def validate(self, dataframe_to_validate):
        summary = {
            'healthy': 0,
            'critical': 0,
            'warning': 0
        }
        details_by_attribute = []

        for column in dataframe_to_validate.columns:
            is_unique = len(dataframe_to_validate[column].unique()) == len(dataframe_to_validate[column])
            column_test_passed = is_unique

            if column_test_passed:
                detail = { 'attribute_name': column }
                summary['healthy'] += 1
                detail['validation_outcome'] = 'healthy'

                details_by_attribute.append(detail)

        return {
            'summary': summary,
            'details_by_attribute': details_by_attribute
        }