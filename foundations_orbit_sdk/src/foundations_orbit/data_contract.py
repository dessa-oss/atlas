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

        self._column_names, self._column_types, self._number_of_rows = self._dataframe_statistics(dataframe)

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
        from foundations_orbit.contract_validators.schema_checker import SchemaChecker
        from foundations_orbit.contract_validators.row_count_checker import RowCountChecker
        from foundations_orbit.contract_validators.distribution_checker import DistributionChecker

        validation_report = {}

        columns_to_validate, types_to_validate, row_count_to_check = self._dataframe_statistics(dataframe_to_validate)

        if self.options.check_schema:
            validation_report['schema_check_results'] = SchemaChecker(self._column_names, self._column_types).schema_check_results(columns_to_validate, types_to_validate)

        if self.options.check_row_count:
            validation_report['row_cnt_diff'] = RowCountChecker(self._number_of_rows).row_count_difference(row_count_to_check)

        if self.options.check_distribution:
            validation_report['dist_check_results'] = DistributionChecker(self.options.distribution).distribution_check_results(columns_to_validate)

        return validation_report

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

    @staticmethod
    def _dataframe_statistics(dataframe):
        column_names = list(dataframe.columns)
        column_types = {column_name: str(dataframe.dtypes[column_name]) for column_name in column_names}
        number_of_rows = len(dataframe)

        return column_names, column_types, number_of_rows