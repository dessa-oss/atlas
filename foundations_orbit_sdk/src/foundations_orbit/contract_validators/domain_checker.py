"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 01 2020
"""


class DomainChecker:
    def __init__(self):
        self._unique_values = {}
        self._configured_attributes = {}

    def __str__(self):
        return str(self.info())

    def info(self):
        return {
            'reference_dataframe_unique': self._unique_values,
            'configured_attributes': self._configured_attributes
        }

    # Validate for DomainChecker returns a data in a different format than the other checkers
    # It is done to reduce complexities in using ReportFormatter and DataContractSummary i.e single source of information
    def validate(self, dataframe_to_validate):
        summary = {
            'healthy': 0,
            'critical': 0,
            'warning': 0
        }
        details_by_attribute = []

        for column, categories in self._configured_attributes.items():
            if categories == ALL_CATEGORIES:
                categories = self._unique_values[column]

            detail = { 'attribute_name': column }
            in_domain_mask = dataframe_to_validate[column].isin(categories)
            column_test_passed = in_domain_mask.all()

            if column_test_passed:
                summary['healthy'] += 1
                detail['validation_outcome'] = 'healthy'
            else:
                summary['critical'] += 1
                detail['validation_outcome'] = 'critical'
                detail['values_out_of_bounds'] = list(dataframe_to_validate[column][~in_domain_mask].unique())
                detail['percentage_out_of_bounds'] = (~in_domain_mask).sum() / in_domain_mask.size

            details_by_attribute.append(detail)

        return {
            'summary': summary,
            'details_by_attribute': details_by_attribute
        }

    def calculate_stats_from_dataframe(self, reference_dataframe):
        import pandas as pd
        for column in reference_dataframe.columns:
            self._unique_values[column] = list(reference_dataframe[column].unique())

    def configure(self, attributes=[], configuration={}):
        if attributes == [] and configuration == {} or attributes != [] and configuration != {}:
            raise ValueError('Please provide only one of attributes or configuration as an argument to configure')

        if attributes != []:
            if type(attributes) is str:
                self._configured_attributes[attributes] = ALL_CATEGORIES
            elif isinstance(attributes, list):
                for attribute in attributes:
                    self._configured_attributes[attribute] = ALL_CATEGORIES
            else:
                raise ValueError('attributes must be of type list or string')
        else:
            if isinstance(configuration, dict):
                for key, value in configuration.items():
                    if not isinstance(key, str):
                        raise ValueError('The column must be of type str')
                    if not (isinstance(value, list) or isinstance(value, str) or value == ALL_CATEGORIES):
                        raise ValueError('The categories must be of type list, str, or AllCategories')
                self._configured_attributes = {**self._configured_attributes, **configuration}
            else:
                raise ValueError('configuration must be of type dict')

    def exclude(self, attributes):
        self._configured_attributes.pop(attributes, None)


ALL_CATEGORIES = 'USE_ALL_CATEGORIES'
