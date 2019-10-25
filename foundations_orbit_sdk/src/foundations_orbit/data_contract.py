"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DataContract(object):

    def __init__(self, contract_name, df=None):
        import pandas
        from foundations_orbit.contract_validators.schema_checker import SchemaChecker
        from foundations_orbit.contract_validators.special_values_checker import SpecialValuesChecker
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats
        from foundations_orbit.contract_validators.distribution_checker import DistributionChecker
        from foundations_orbit.contract_validators.min_max_checker import MinMaxChecker

        self.options = self._default_options()
        self._contract_name = contract_name

        if df is None:
            raise ValueError('Reference DataFrame Not Provided')
        else:
            self._dataframe = df

        self._column_names, self._column_types, self._number_of_rows = self._dataframe_statistics(self._dataframe)
        self.schema_test = SchemaChecker(self._column_names, self._column_types)
        self._remove_object_columns_and_types(self._column_names, self._column_types)

        self._bin_stats = {column_name: create_bin_stats(self.options.special_values, self.options.max_bins, self._dataframe[column_name]) for column_name in self._column_names}

        self.special_value_test = SpecialValuesChecker(self.options, self._bin_stats, self._column_names, self._column_types, self._dataframe)
        self.distribution_test = DistributionChecker(self.options.distribution, self._bin_stats, self._column_names)
        self.min_max_test = MinMaxChecker(self._column_types)

    @staticmethod
    def _default_options():
        import numpy
        from foundations_orbit.data_contract_options import DataContractOptions

        default_distribution = {
            'distance_metric': 'l_infinity',
            'default_threshold': 0.1,
            'cols_to_include': None,
            'cols_to_ignore': None,
            'custom_thresholds': {},
            'custom_methods': {},
            'special_value_thresholds': {}
        }

        return DataContractOptions(
            max_bins=50,
            check_row_count=True,
            special_values=[numpy.nan],
            check_distribution=True,
            check_special_values=True,
            check_min_max=True,
            distribution=default_distribution
        )

    def save(self, monitor_package_directory):
        with open(self._data_contract_file_path(monitor_package_directory), 'wb') as contract_file:
            contract_file.write(self._serialized_contract())

    @staticmethod
    def load(monitor_package_directory, contract_name):
        import pickle

        data_contract_file_name = DataContract._data_contract_file_path_with_contract_name(monitor_package_directory, contract_name)
        with open(data_contract_file_name, 'rb') as contract_file:
            return DataContract._deserialized_contract(contract_file.read())

    def _save_to_redis(self, project_name, monitor_name, contract_name, inference_period, serialized_output, summary):
        from foundations_contrib.global_state import redis_connection
        key = f'projects:{project_name}:monitors:{monitor_name}:validation:{contract_name}'
        counter_key = f'projects:{project_name}:monitors:{monitor_name}:validation:{contract_name}:counter'
        summary_key = f'projects:{project_name}:monitors:{monitor_name}:validation:{contract_name}:summary'
        redis_connection.hset(key, inference_period, serialized_output)
        redis_connection.hset(summary_key, inference_period, summary)
        redis_connection.incr(counter_key)

    def validate(self, dataframe_to_validate, inference_period=None):
        import datetime
        import os
        from uuid import uuid4
        from getpass import getuser

        from foundations_orbit.contract_validators.row_count_checker import RowCountChecker
        from foundations_orbit.contract_validators.special_values_checker import SpecialValuesChecker
        from foundations_orbit.data_contract_summary import DataContractSummary
        from foundations_orbit.report_formatter import ReportFormatter

        project_name = os.environ.get('PROJECT_NAME', 'default')
        monitor_name = os.environ.get('MONITOR_NAME', os.path.basename(__file__))
        user = os.environ.get('FOUNDATIONS_USER', getuser())
        job_id = os.environ.get('FOUNDATIONS_JOB_ID', str(uuid4()))
        
        if inference_period is None:
            inference_period = str(datetime.datetime.now())

        columns_to_validate, types_to_validate, row_count_to_check = self._dataframe_statistics(dataframe_to_validate)

        validation_report = {}
        validation_report['schema_check_results'] = self.schema_test.validate(dataframe_to_validate)

        if self.options.check_row_count:
            validation_report['row_count'] = RowCountChecker(self._number_of_rows).validate(dataframe_to_validate)

        if self.options.check_distribution:
            validation_report['dist_check_results'] = self.distribution_test.validate(dataframe_to_validate)

        if self.options.check_special_values:
            validation_report['special_values_check_results'] = self.special_value_test.validate(dataframe_to_validate)

        if self.options.check_min_max:
            validation_report['min_max_test_results'] = self.min_max_test.validate(dataframe_to_validate)

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

        report_formatter = ReportFormatter(inference_period=inference_period,
                                    monitor_package=monitor_name,
                                    contract_name=self._contract_name,
                                    job_id=job_id,
                                    user=user,
                                    validation_report=validation_report,
                                    options=self.options)
        serialized_output = report_formatter.serialized_output()

        data_contract_summary = DataContractSummary(report_formatter.formatted_report())

        self._save_to_redis(project_name, monitor_name, self._contract_name, inference_period, serialized_output, data_contract_summary.serialized_output())

        return validation_report

    def __eq__(self, other):
        return self._contract_name == other._contract_name and self.options == other.options

    def _data_contract_file_path(self, monitor_package_directory):
        return self._data_contract_file_path_with_contract_name(monitor_package_directory, self._contract_name)

    @staticmethod
    def _data_contract_file_path_with_contract_name(monitor_package_directory, contract_name):
        return f'{monitor_package_directory}/{contract_name}.pkl'

    def _serialized_contract(self):
        import pickle
        return pickle.dumps(self)

    @staticmethod
    def _deserialized_contract(serialized_contract):
        import pickle
        return pickle.loads(serialized_contract)

    @staticmethod
    def _dataframe_statistics(dataframe):
        import numpy
        column_names = list(dataframe.columns)
        column_types = {column_name: str(dataframe.dtypes[column_name]) for column_name in column_names}
        number_of_rows = len(dataframe)

        for col_name, col_type in column_types.items():
            if col_type == "object":
                object_type_column = dataframe[col_name]
                string_column_mask = [type(value) == str or numpy.isnan(value) for value in object_type_column]
                if all(string_column_mask):
                    column_types[col_name] = "str"

        return column_names, column_types, number_of_rows

    @staticmethod
    def _remove_object_columns_and_types(column_names, column_types):
        column_names_to_delete = []
        for column_name, column_type in column_types.items():
            if column_type == 'object':
                column_names.remove(column_name)
                column_names_to_delete.append(column_name)

        for column_name in column_names_to_delete:
            column_types.pop(column_name)