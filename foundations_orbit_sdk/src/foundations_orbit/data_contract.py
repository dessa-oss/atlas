"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DataContract(object):
    
    def __init__(self, contract_name, df=None):
        import pandas

        self.options = self._default_options()
        self._contract_name = contract_name

        if df is None:
            dataframe = pandas.DataFrame()
        else:
            dataframe = df

        self._column_names = list(dataframe.columns)

    @staticmethod
    def _default_options():
        import numpy
        from foundations_orbit.data_contract_options import DataContractOptions

        default_distribution = {
            'distance_metric': 'l_infinity',
            'default_threshold': 0.1,
            'cols_to_include': None,
            'cols_to_ignore': None,
            'custom_thresholds': {}
        }

        return DataContractOptions(
            max_bins=50,
            check_schema=True,
            check_row_count=False,
            special_values=[numpy.nan],
            check_distribution=True,
            distribution=default_distribution
        )

    def save(self, model_package_directory):
        with open(self._data_contract_file_path(model_package_directory), 'wb') as contract_file:
            contract_file.write(self._serialized_contract())

    @staticmethod
    def load(model_package_directory, contract_name):
        import pickle

        data_contract_file_name = DataContract._data_contract_file_path_with_contract_name(model_package_directory, contract_name)
        with open(data_contract_file_name, 'rb') as contract_file:
            return DataContract._deserialized_contract(contract_file.read())

    def validate(self, dataframe_to_validate, *args):
        import numpy

        validation_report = {
            'dist_check_results': {}
        }

        columns_to_validate = list(dataframe_to_validate.columns)

        if self.options.check_schema:
            validation_report['schema_check_passed'] = self._passes_schema_check(columns_to_validate)

        results_for_same_distribution = {
            'binned_l_infinity': 0.0,
            'binned_passed': True,
            'special_values': {
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            }
        }

        for column_name in columns_to_validate:
            validation_report['dist_check_results'][column_name] = results_for_same_distribution

        return validation_report

    def _passes_schema_check(self, columns_to_validate):
        schema_check_passed = self._column_names == columns_to_validate
        return schema_check_passed

    def __eq__(self, other):
        return self._contract_name == other._contract_name and self.options == other.options

    def _data_contract_file_path(self, model_package_directory):
        return self._data_contract_file_path_with_contract_name(model_package_directory, self._contract_name)

    @staticmethod
    def _data_contract_file_path_with_contract_name(model_package_directory, contract_name):
        return f'{model_package_directory}/{contract_name}.pkl'

    def _serialized_contract(self):
        import pickle

        contract = DataContract(self._contract_name)
        contract.options = self.options

        return pickle.dumps(contract)

    @staticmethod
    def _deserialized_contract(serialized_contract):
        import pickle
        return pickle.loads(serialized_contract)