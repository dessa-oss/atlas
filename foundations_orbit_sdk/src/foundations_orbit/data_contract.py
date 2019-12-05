"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DataContract(object):

    def __init__(self, contract_name, df=None):
        from foundations_orbit.data_contract_summary import DataContractSummary
        from foundations_orbit.utils.get_column_types import get_column_types
        import uuid

        self.options = self._default_options()
        self._contract_name = contract_name

        if df is None:
            raise ValueError('Reference DataFrame Not Provided')
        else:
            self._dataframe = df

        self.bin_stats_calculated = False

        self._number_of_rows = len(self._dataframe)
        self._column_names, self._column_types = get_column_types(self._dataframe)
        self._bin_stats = {}
        self._uuid = uuid.uuid4()

        self._categorical_attributes = {}
        self._categorize_attributes()

        self._initialize_checkers()
        self.summary = DataContractSummary(self._dataframe, self._column_names, self._column_types, self._categorical_attributes)

    def __str__(self):
        return str(self.info())

    def info(self):
        return {
            'special_values_test': self.special_value_test.info(),
            'min_max_test': self.min_max_test.info(),
            'distribution_test': self.distribution_test.info(),
            'schema_test': self.schema_test.info()
        }

    @staticmethod
    def _default_options():
        from foundations_orbit.data_contract_options import DataContractOptions

        return DataContractOptions(
            check_row_count=True,
            check_distribution=True,
            check_special_values=True,
            check_min_max=True,
        )

    def _initialize_checkers(self):
        from foundations_orbit.contract_validators.special_values_checker import SpecialValuesChecker
        from foundations_orbit.contract_validators.distribution_checker import DistributionChecker
        from foundations_orbit.contract_validators.min_max_checker import MinMaxChecker
        self._initialize_schema_checker()

        self.special_value_test = SpecialValuesChecker(self._column_names, self._column_types, self._categorical_attributes)
        self.distribution_test = DistributionChecker(self._column_names, self._column_types, self._categorical_attributes)

        self.min_max_test = MinMaxChecker(self._column_types)

    def _categorize_attributes(self):
        for col_name, col_type in self._column_types.items():
            if 'float' in col_type:
                self._categorical_attributes[col_name] = False
            elif 'int' in col_type:
                self._categorical_attributes[col_name] = self._check_if_attribute_is_categorical(col_name)
            elif 'str' in col_type:
                self._categorical_attributes[col_name] = self._check_if_attribute_is_categorical(col_name, threshold=0.5)
            elif 'bool' in col_type:
                self._categorical_attributes[col_name] = True
            elif 'datetime' in col_type:
                self._categorical_attributes[col_name] = self._check_if_attribute_is_categorical(col_name)
            elif 'category' in col_type:
                self._categorical_attributes[col_name] = True
            elif 'object' in col_type:
                self._categorical_attributes[col_name] = False

    def _initialize_schema_checker(self):
        from foundations_orbit.contract_validators.schema_checker import SchemaChecker
        self.schema_test = SchemaChecker(self._column_names, self._column_types)

    def _check_if_attribute_is_categorical(self, column_name, threshold=0.1):
        column_values = self._dataframe[column_name]
        num_unique_values = column_values.nunique()
        num_total_values = len(column_values)
        if num_unique_values/num_total_values > threshold: 
            return False
        return True

    def exclude(self, attributes):
        if type(attributes) == str:
            attributes = [attributes]

        self.special_value_test.exclude(attributes=attributes)# TODO change this to columns for consistency
        self.distribution_test.exclude(attributes=attributes)# TODO change this to columns for consistency
        self.min_max_test.exclude(attributes=attributes)

    def _exclude_from_current_validation(self, attributes):
        if type(attributes) == str:
            attributes = [attributes]

        self.special_value_test.temp_exclude(attributes=attributes)
        self.distribution_test.temp_exclude(attributes=attributes)
        self.min_max_test.schema_failure_temp_exclusion(columns=attributes)   # TODO change this to attributes for consistency

    def save(self, monitor_package_directory):
        if not self._bin_stats:
            self.set_bin_stats()

        del self._dataframe

        with open(self._data_contract_file_path(monitor_package_directory), 'wb') as contract_file:
            contract_file.write(self._serialized_contract())

    @staticmethod
    def load(monitor_package_directory, contract_name):
        data_contract_file_name = DataContract._data_contract_file_path_with_contract_name(monitor_package_directory, contract_name)
        with open(data_contract_file_name, 'rb') as contract_file:
            return DataContract._deserialized_contract(contract_file.read())

    def _save_to_redis(self, project_name, monitor_name, contract_name, inference_period, serialized_output, summary):
        from foundations_contrib.global_state import redis_connection

        key = f'projects:{project_name}:monitors:{monitor_name}:validation:{contract_name}'
        counter_key = f'projects:{project_name}:monitors:{monitor_name}:validation:{contract_name}:counter'
        summary_key = f'projects:{project_name}:monitors:{monitor_name}:validation:{contract_name}:summary'
        id_key = f'projects:{project_name}:monitors:{monitor_name}:validation:{contract_name}:id'

        redis_connection.hset(key, inference_period, serialized_output)
        redis_connection.hset(summary_key, inference_period, summary)
        redis_connection.set(id_key, str(self._uuid))
        redis_connection.incr(counter_key)

        self._save_all_contract_info_to_redis(project_name, monitor_name, contract_name)

    def _save_all_contract_info_to_redis(self, project_name, monitor_name, contract_name):
        from foundations_contrib.global_state import redis_connection
        import json

        info_key = f'contracts:{self._uuid}:info'
        redis_connection.set(info_key, json.dumps(self.info(), default=str, indent=4))

        self._set_contract_info_to_redis('project_name', project_name)
        self._set_contract_info_to_redis('monitor_name', monitor_name)
        self._set_contract_info_to_redis('contract_name', contract_name)

    def _set_contract_info_to_redis(self, key, value):
        from foundations_contrib.global_state import redis_connection
        
        key = f'contracts:{self._uuid}:{key}'
        redis_connection.set(key, value)

    def validate(self, dataframe_to_validate, inference_period=None):
        import datetime
        import os
        from uuid import uuid4
        from getpass import getuser
        from redis import ConnectionError
        import inspect

        from foundations_orbit.report_formatter import ReportFormatter
        from foundations_orbit.utils.get_column_types import get_column_types
        from foundations_contrib.utils import save_project_to_redis

        if not self._bin_stats:
            self.set_bin_stats()

        caller_stackframe = inspect.stack()[1]
        caller_module_name = inspect.getmodule(caller_stackframe[0])
        default_filename = os.path.basename(caller_module_name.__file__)

        project_name = os.environ.get('PROJECT_NAME', 'default')
        monitor_name = os.environ.get('MONITOR_NAME', default_filename)
        user = os.environ.get('FOUNDATIONS_USER', getuser())
        job_id = os.environ.get('FOUNDATIONS_JOB_ID', str(uuid4()))

        if inference_period is None:
            inference_period = str(datetime.datetime.now())

        inference_period = str(inference_period)

        columns_to_validate, types_to_validate = get_column_types(dataframe_to_validate)
        
        attributes_to_ignore = []
        validation_report = self._run_checkers_and_get_validation_report(dataframe_to_validate, attributes_to_ignore)
        self._add_metadata_to_validation_report(validation_report, columns_to_validate, types_to_validate)

        report_formatter = ReportFormatter(inference_period=inference_period,
                                    monitor_package=monitor_name,
                                    contract_name=self._contract_name,
                                    job_id=job_id,
                                    user=user,
                                    validation_report=validation_report,
                                    options=self.options)
        serialized_output = report_formatter.serialized_output()

        self.summary.validate(dataframe_to_validate, report_formatter.formatted_report())

        try:
            save_project_to_redis(project_name)
            self._save_to_redis(project_name, monitor_name, self._contract_name, inference_period, serialized_output, self.summary.serialized_output())
        except ConnectionError as e:
            self._log().warn('WARNING: Unable to connect to redis. Data contract results will not be saved')

        self._modify_validation_report_with_schema_failures(validation_report, attributes_to_ignore)

        return validation_report

    def _run_checkers_and_get_validation_report(self, dataframe_to_validate, attributes_to_ignore):
        from foundations_orbit.contract_validators.row_count_checker import RowCountChecker

        validation_report = {
            'schema_check_results': self.schema_test.validate(dataframe_to_validate)
        }

        if not validation_report['schema_check_results']['passed'] and validation_report['schema_check_results'].get('cols', None):
            for column_to_ignore in validation_report['schema_check_results']['cols'].keys():
                attributes_to_ignore.append(column_to_ignore)
            self._exclude_from_current_validation(attributes=attributes_to_ignore)

        if self.options.check_row_count:
            validation_report['row_count'] = RowCountChecker(self._number_of_rows).validate(dataframe_to_validate)

        if self.options.check_distribution:
            validation_report['dist_check_results'] = self.distribution_test.validate(dataframe_to_validate)

        if self.options.check_special_values:
            validation_report['special_values_check_results'] = self.special_value_test.validate(dataframe_to_validate)

        if self.options.check_min_max:
            validation_report['min_max_test_results'] = self.min_max_test.validate(dataframe_to_validate)

        return validation_report

    def _add_metadata_to_validation_report(self, validation_report, columns_to_validate, types_to_validate):

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

    def set_bin_stats(self):
        if not self.bin_stats_calculated:
            self.special_value_test.create_and_set_special_value_percentages(self._dataframe)
            self.distribution_test.create_and_set_bin_stats(self._dataframe)
            self.bin_stats_calculated = True

    def _modify_validation_report_with_schema_failures(self, validation_report, attributes_to_ignore):
        for test_name, test_dictionary in validation_report.items():
            if test_name == 'dist_check_results':
                for attribute in attributes_to_ignore:
                    test_dictionary[attribute] = {"binned_passed": False, "message": "Schema Test Failed"}
            elif test_name == 'special_values_check_results':
                for attribute in attributes_to_ignore:
                    test_dictionary[attribute] = {"passed": False, "message": "Schema Test Failed"}
            elif test_name == 'special_values_check_results':
                for attribute in attributes_to_ignore:
                    test_dictionary[attribute]['min_test'] = {"passed": False, "message": "Schema Test Failed"}
                    test_dictionary[attribute]['max_test'] = {"passed": False, "message": "Schema Test Failed"}

    @staticmethod
    def _log():
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)

