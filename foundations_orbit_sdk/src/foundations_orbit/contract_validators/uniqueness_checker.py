
import pandas as pd
import numpy as np
class UniquenessChecker:

    def __init__(self):
        self._configured_attributes = set()

    def __str__(self):
        return str(self.info())

    def info(self):
        return {
            'configured_attributes': self._configured_attributes
        }
    
    def validate(self, dataframe_to_validate):

        summary = {
            'healthy': 0,
            'critical': 0,
            'warning': 0
        }
        details_by_attribute = []

        dataframe_to_validate = dataframe_to_validate[list(self._configured_attributes)]

        dataframe_duplication_mask = dataframe_to_validate.apply(pd.Series.duplicated, keep=False)
        number_of_duplicates = dataframe_duplication_mask.sum()

        duplicate_values_dataframe = dataframe_to_validate.mask(~dataframe_duplication_mask)

        for column in dataframe_to_validate.columns:
            is_unique = number_of_duplicates[column] == 0

            detail = { 'attribute_name': column }

            if is_unique:
                summary['healthy'] += 1
                detail['validation_outcome'] = 'healthy'
            else:
                summary['critical'] += 1
                detail['validation_outcome'] = 'critical'
                detail['percentage_of_duplicates'] = float(number_of_duplicates[column] / dataframe_to_validate[column].size)
                detail['duplicate_values'] = duplicate_values_dataframe[column].dropna().unique().tolist()

            details_by_attribute.append(detail)

        return {
            'summary': summary,
            'details_by_attribute': details_by_attribute
        }

    def exclude(self, attributes):
        if type(attributes) == str:
            self._configured_attributes.remove(attributes)
        elif type(attributes) == list:
            self._configured_attributes = self._configured_attributes.difference(attributes)
        else:
            raise ValueError('Please provide only one of attributes or configuration as an argument to configure')

    def configure(self, attributes):
        if type(attributes) == str:
            self._configured_attributes.add(attributes)
        elif type(attributes) == list:
            self._configured_attributes.update(attributes)
        else:
            raise ValueError('Please provide only one of attributes or configuration as an argument to configure')