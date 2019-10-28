"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DataContractSummary(object):

    def __init__(self, dataframe, column_names, column_types):
        self._num_critical_tests = 0
        self._report = None
        self._tests_to_summarize = ['schema', 'data_quality', 'population_shift', 'min', 'max']
        self._dataframe = dataframe
        self._attributes = column_names
        self._column_types = column_types
        self.data_contract_summary = {'attribute_summaries': {}}
        self._expected_data_bin_by_attribute = {}
        self._summarize_expected_data()

    def validate(self, dataframe_to_validate, formatted_validation_report):
        self._num_critical_tests = 0
        self._report = formatted_validation_report
        self._summarize_num_critical()
        self._summarize_actual_data(dataframe_to_validate)

    def _summarize_num_critical(self):
        for test in self._tests_to_summarize:
            if 'summary' in self._report[test] and self._report[test]['summary']['critical'] > 0:
                self._num_critical_tests += 1
        self.data_contract_summary['num_critical_tests'] = self._num_critical_tests

    def _summarize_expected_data(self):
        for attribute in self._attributes:
            self.data_contract_summary['attribute_summaries'][attribute] = self._summarize_attribute_expected_data(attribute)

    def _summarize_actual_data(self, dataframe_to_validate):
        for attribute in self._attributes:
            self._summarize_attribute_actual_data(dataframe_to_validate, attribute)

    @staticmethod
    def _is_numeric_column(column_type):
        return any([numeric_type in column_type for numeric_type in ['int', 'float']])

    def _summarize_attribute_expected_data(self, attribute):
        column_type = self._column_types[attribute]
        if not self._is_numeric_column(column_type):
            return {'expected_data_summary': None, 'binned_data': {'bins': None, 'data': {'expected_data': None}}}

        attribute_summaries = {'expected_data_summary': {
            'percentage_missing': self._calculate_percentage_missing(self._dataframe, attribute),
            'minimum': self._calculate_minimum(self._dataframe, attribute),
            'maximum': self._calculate_maximum(self._dataframe, attribute)
        }, 'binned_data': self._bin_data(attribute, column_type)}

        return attribute_summaries

    def _summarize_attribute_actual_data(self, dataframe_to_validate, attribute):
        column_type = self._column_types.get(attribute, 'missing_column')

        if attribute not in dataframe_to_validate.columns or dataframe_to_validate[attribute].dtype != column_type or not self._is_numeric_column(column_type):
            self.data_contract_summary['attribute_summaries'][attribute]['actual_data_summary'] = None
            self.data_contract_summary['attribute_summaries'][attribute]['binned_data']['data']['actual_data'] = None
            return

        self.data_contract_summary['attribute_summaries'][attribute]['actual_data_summary'] = {
            'percentage_missing': self._calculate_percentage_missing(dataframe_to_validate, attribute),
            'minimum': self._calculate_minimum(dataframe_to_validate, attribute),
            'maximum': self._calculate_maximum(dataframe_to_validate, attribute)
        }

        self.data_contract_summary['attribute_summaries'][attribute]['binned_data']['data']['actual_data'] = self._validate_binned_data(dataframe_to_validate, attribute, column_type)

    @staticmethod
    def _calculate_percentage_missing(dataframe, attribute):
        return DataContractSummary._numpy_type_to_python(dataframe[attribute].isna().sum() / len(dataframe[attribute]))

    @staticmethod
    def _calculate_minimum(dataframe, attribute):
        return DataContractSummary._numpy_type_to_python(dataframe[attribute].min())

    @staticmethod
    def _calculate_maximum(dataframe, attribute):
        return DataContractSummary._numpy_type_to_python(dataframe[attribute].max())

    @staticmethod
    def _numpy_type_to_python(value):
        if type(value) == list:
            return list(map(lambda v: float(v), value))
        return float(value)

    @staticmethod
    def _get_bins_and_data_for_numerical_attribute(dataframe, attribute, bins=10):
        import numpy as np
        data, bins = np.histogram(dataframe[attribute].dropna(), bins=bins)
        return bins, data

    def _bin_data(self, attribute, attribute_type):
        bins = []
        data = []
        if self._is_numeric_column(attribute_type):
            bins, data = self._get_bins_and_data_for_numerical_attribute(self._dataframe, attribute)
            self._expected_data_bin_by_attribute[attribute] = bins
        # TODO - Add implementation for object dtypes
        bin_labels = [f'{round(bound1, 2)}-{round(bound2, 2)}' for bound1, bound2 in zip(bins, bins[1:])]
        return {
            'bins': bin_labels,
            'data': {
                'expected_data': self._numpy_type_to_python(list(data))
            }
        }

    def _validate_binned_data(self, dataframe_to_validate, attribute, attribute_type):
        data = []
        expected_bins = self._expected_data_bin_by_attribute[attribute]
        if self._is_numeric_column(attribute_type):
            _, data = self._get_bins_and_data_for_numerical_attribute(dataframe_to_validate, attribute, bins=expected_bins)
        # TODO - Add implementation for object dtypes
        return self._numpy_type_to_python(list(data))

    def serialized_output(self):
        import pickle

        return pickle.dumps(self.data_contract_summary)