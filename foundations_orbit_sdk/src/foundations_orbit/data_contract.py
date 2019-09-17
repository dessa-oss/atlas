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
            self._dataframe = pandas.DataFrame()
        else:
            self._dataframe = df

        self._column_names = None
        self._column_types = None
        self._number_of_rows = None
        self._bin_stats = None

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

    def _save_to_redis(self, project_name, model_name, contract_name, inference_period, serialized_output):
        from foundations_contrib.global_state import redis_connection
        key = f'projects:{project_name}:models:{model_name}:validation:{contract_name}'
        redis_connection.hset(key, inference_period, serialized_output)

    def validate(self, dataframe_to_validate, inference_period=None):
        from foundations_orbit.contract_validators.schema_checker import SchemaChecker
        from foundations_orbit.contract_validators.row_count_checker import RowCountChecker
        # from foundations_orbit.contract_validators.distribution_checker import DistributionChecker

        self._column_names, self._column_types, self._number_of_rows = self._dataframe_statistics(self._dataframe)

        ##### PROTOTYPE CODE - REMOVE ME PLEASE

        from foundations_orbit.contract_validators.prototype import create_bin_stats

        self._bin_stats = {column_name: create_bin_stats(self.options.special_values, self.options.max_bins, self._dataframe[column_name]) for column_name in self._column_names}

        import datetime
        from foundations_orbit.contract_validators.prototype import distribution_check, output_for_writing, write_to_redis

        if inference_period is None:
            inference_period = str(datetime.datetime.now())

        validation_report = {}

        columns_to_validate, types_to_validate, row_count_to_check = self._dataframe_statistics(dataframe_to_validate)

        ##### Prototype code section end

        validation_report['schema_check_results'] = SchemaChecker(self._column_names, self._column_types).schema_check_results(columns_to_validate, types_to_validate)

        if self.options.check_row_count:
            validation_report['row_cnt_diff'] = RowCountChecker(self._number_of_rows).row_count_difference(row_count_to_check)

        if self.options.check_distribution:
            ##### PROTOTYPE CODE - use distribution checker asap
            validation_report['dist_check_results'] = distribution_check(self.options.distribution, self._column_names, self._bin_stats, dataframe_to_validate)

        validation_report['metadata'] = {
            'reference_metadata': {
                'column_names': self._column_names,
                'type_mapping': self._column_types
            },
            'current_metadata': {
                'column_names': columns_to_validate,
                'type_mapping': types_to_validate
            }
        }

        ##### PROTOTYPE CODE - replace with robust private methods
        import os

        project_name = os.environ['PROJECT_NAME']
        model_name = os.environ['MODEL_NAME']

        row_cnt_diff = validation_report.get('row_cnt_diff', 0)
        schema_check_results = validation_report.get('schema_check_results', {})
        schema_check_passed = schema_check_results.get('passed', True)
        dist_check_results = validation_report.get('dist_check_results', {})

        schema_check_failure_dict = schema_check_results.copy()
        if 'passed' in schema_check_failure_dict:
            schema_check_failure_dict.pop('passed')

        output_to_write = output_for_writing(
            inference_period,
            model_name,
            self._contract_name,
            row_cnt_diff,
            schema_check_passed,
            len(self._column_names),
            schema_check_failure_dict,
            len(columns_to_validate),
            types_to_validate,
            self._column_types,
            self.options.check_distribution,
            dist_check_results,
            self.options.special_values
        )

        self._save_to_redis(project_name, model_name, self._contract_name, inference_period, output_to_write)

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
        return pickle.dumps(self)

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