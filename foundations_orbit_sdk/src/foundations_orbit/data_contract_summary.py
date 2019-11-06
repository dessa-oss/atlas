"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DataContractSummary(object):

    def __init__(self, dataframe, column_names, column_types, categorical_columns=None):
        self._num_critical_tests = 0
        self._report = None
        self._bins_were_cut_off = False
        self._current_column_types = None
        self._tests_to_summarize = ['schema', 'data_quality', 'population_shift', 'min', 'max']
        self._attributes = column_names
        self._column_types = column_types
        self._categorical_columns = categorical_columns
        self.data_contract_summary = {'attribute_summaries': {}}
        self._expected_data_bin_by_attribute = {}
        self._summarize_expected_data(dataframe)

    def validate(self, dataframe_to_validate, formatted_validation_report):
        from foundations_orbit.utils.get_column_types import get_column_types
        self._num_critical_tests = 0
        self._report = formatted_validation_report
        _, self._current_column_types = get_column_types(dataframe_to_validate)
        self._summarize_num_critical()
        self._summarize_actual_data(dataframe_to_validate)

    def _summarize_num_critical(self):
        for test in self._tests_to_summarize:
            if 'summary' in self._report[test] and self._report[test]['summary']['critical'] > 0:
                self._num_critical_tests += 1
        self.data_contract_summary['num_critical_tests'] = self._num_critical_tests

    def _summarize_expected_data(self, reference_dataframe):
        for attribute in self._attributes:
            self.data_contract_summary['attribute_summaries'][attribute] = self._summarize_attribute_expected_data(attribute, reference_dataframe)

    def _summarize_actual_data(self, dataframe_to_validate):
        for attribute in self._attributes:
            self._summarize_attribute_actual_data(dataframe_to_validate, attribute)

    @staticmethod
    def _is_numeric_column(column_type):
        return any([numeric_type in column_type for numeric_type in ['int', 'float']])

    def _is_categorical_column(self, column):
        return self._categorical_columns and column in self._categorical_columns and self._categorical_columns[column]

    def _summarize_attribute_expected_data(self, attribute, reference_dataframe):
        column_type = self._column_types[attribute]
        if not self._is_numeric_column(column_type) and not self._is_categorical_column(attribute):
            return {'expected_data_summary': None, 'binned_data': {'bins': None, 'data': {'expected_data': None}}}

        attribute_summaries = {'expected_data_summary': {
            'percentage_missing': self._calculate_percentage_missing(reference_dataframe, attribute),
            'minimum': self._calculate_minimum(reference_dataframe, attribute, column_type),
            'maximum': self._calculate_maximum(reference_dataframe, attribute, column_type)
        }, 'binned_data': self._bin_data(attribute, column_type, reference_dataframe)}

        return attribute_summaries

    def _summarize_attribute_actual_data(self, dataframe_to_validate, attribute):
        column_type = self._column_types.get(attribute, 'missing_column')

        if attribute not in dataframe_to_validate.columns or self._current_column_types[attribute] != column_type or not (self._is_numeric_column(column_type) or self._is_categorical_column(attribute)):
            self.data_contract_summary['attribute_summaries'][attribute]['actual_data_summary'] = None
            self.data_contract_summary['attribute_summaries'][attribute]['binned_data']['data']['actual_data'] = None
            return

        self.data_contract_summary['attribute_summaries'][attribute]['actual_data_summary'] = {
            'percentage_missing': self._calculate_percentage_missing(dataframe_to_validate, attribute),
            'minimum': self._calculate_minimum(dataframe_to_validate, attribute, column_type),
            'maximum': self._calculate_maximum(dataframe_to_validate, attribute, column_type)
        }

        self.data_contract_summary['attribute_summaries'][attribute]['binned_data']['data']['actual_data'] = self._validate_binned_data(dataframe_to_validate, attribute, column_type)

    @staticmethod
    def _calculate_percentage_missing(dataframe, attribute):
        return DataContractSummary._numpy_type_to_python(dataframe[attribute].isna().sum() / len(dataframe[attribute]))

    @staticmethod
    def _calculate_minimum(dataframe, attribute, column_type):
        if 'str' in column_type or 'bool' in column_type:
            return None
        return DataContractSummary._numpy_type_to_python(dataframe[attribute].min())

    @staticmethod
    def _calculate_maximum(dataframe, attribute, column_type):
        if 'str' in column_type or 'bool' in column_type:
            return None
        return DataContractSummary._numpy_type_to_python(dataframe[attribute].max())

    @staticmethod
    def _numpy_type_to_python(value):
        if type(value) == list:
            return list(map(lambda v: float(v), value))
        elif 'timestamp' in str(type(value)):
            return value.to_pydatetime()
        return float(value)

    @staticmethod
    def _get_bins_and_data_for_numerical_attribute(dataframe, attribute, bins=10):
        import numpy as np
        data, bins = np.histogram(dataframe[attribute].dropna(), bins=bins)
        return bins, data

    def _get_bins_and_data_for_categorical_attribute(self, dataframe, attribute):
        import numpy as np
        value_counts = dataframe[attribute].value_counts()
        bins = value_counts.keys().tolist()
        data = value_counts.tolist()

        if (len(bins) > 10):
            self._bins_were_cut_off = True
            bins = bins[:9]
            bins.append('Other')
            other_data = sum(data[9:])
            data = data[:9]
            data.append(other_data)

        return bins, data

    def _get_bin_counts_for_categorical_attribute(self, dataframe, attribute, expected_bins):
        value_counts = dict(dataframe[attribute].value_counts())
        if self._bins_were_cut_off:
            expected_bins = expected_bins[:-1]
        
        counts = []
        for bin in expected_bins:
            counts.append(value_counts.pop(bin, 0))
        
        if self._bins_were_cut_off:
            counts.append(sum(value_counts.values()))
        
        return counts

    def _bin_data(self, attribute, attribute_type, reference_dataframe):
        bins = []
        data = []

        if self._is_categorical_column(attribute):
            bins, data = self._get_bins_and_data_for_categorical_attribute(reference_dataframe, attribute)
            bin_labels = bins
        elif self._is_numeric_column(attribute_type):
            bins, data = self._get_bins_and_data_for_numerical_attribute(reference_dataframe, attribute)
            bin_labels = [f'{round(bound1, 2)}-{round(bound2, 2)}' for bound1, bound2 in zip(bins, bins[1:])]

        self._expected_data_bin_by_attribute[attribute] = bins
        return {
            'bins': bin_labels,
            'data': {
                'expected_data': self._numpy_type_to_python(list(data))
            }
        }

    def _validate_binned_data(self, dataframe_to_validate, attribute, attribute_type):
        data = []
        expected_bins = self._expected_data_bin_by_attribute[attribute]

        if self._is_categorical_column(attribute):
            data = self._get_bin_counts_for_categorical_attribute(dataframe_to_validate, attribute, expected_bins)
        elif self._is_numeric_column(attribute_type):
            _, data = self._get_bins_and_data_for_numerical_attribute(dataframe_to_validate, attribute, bins=expected_bins)
        return self._numpy_type_to_python(list(data))

    def serialized_output(self):
        import pickle

        return pickle.dumps(self.data_contract_summary)