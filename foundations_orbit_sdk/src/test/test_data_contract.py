"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import fakeredis
from foundations_orbit.data_contract import DataContract

class TestDataContract(Spec):

    mock_open = let_patch_mock_with_conditional_return('builtins.open')
    mock_file_for_write = let_mock()
    mock_file_for_read = let_mock()

    @let
    def contract_name(self):
        return self.faker.word()

    @let
    def other_contract_name(self):
        return self._generate_distinct([self.contract_name], self.faker.word)

    @let
    def monitor_package_directory(self):
        return self.faker.file_path()

    @let
    def data_contract_file_path(self):
        return f'{self.monitor_package_directory}/{self.contract_name}.pkl'

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def model_name(self):
        return self.faker.word()

    @let_now
    def datetime_today(self):
        import datetime
        return datetime.datetime.today()

    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()

    @let
    def column_name(self):
        return self.faker.word()

    @let
    def column_name_2(self):
        return self._generate_distinct([self.column_name], self.faker.word)

    @let
    def column_name_3(self):
        return self._generate_distinct([self.column_name, self.column_name_2], self.faker.word)

    @let
    def column_name_4(self):
        return self._generate_distinct([self.column_name, self.column_name_2, self.column_name_3], self.faker.word)

    @let
    def column_name_5(self):
        return self._generate_distinct([self.column_name, self.column_name_2, self.column_name_3, self.column_name_4], self.faker.word)

    @let
    def row_count_results(self):
        return self.faker.random.random()
    
    @let
    def bin_return_value(self):
        return {'percentage': .5, 'upper_edge': None}

    @let
    def inference_period(self):
        return '2019-07-06'

    @let
    def bin_stats(self):
        return {
            self.column_name: self.bin_return_value,
            self.column_name_2: self.bin_return_value
        }

    @let_now
    def one_column_dataframe(self):
        import numpy
        import pandas

        return pandas.DataFrame(columns=[self.column_name], data=[4], dtype=numpy.int8)

    @let_now
    def one_column_dataframe_two_rows(self):
        import numpy
        import pandas

        return pandas.DataFrame(columns=[self.column_name], data=[4, 5], dtype=numpy.int8)

    @let_now
    def one_column_dataframe_four_rows(self):
        import numpy
        import pandas

        return pandas.DataFrame(columns=[self.column_name], data=[4, 5, 6, 7], dtype=numpy.int8)

    @let_now
    def one_column_dataframe_different_data_type(self):
        import numpy
        import pandas

        return pandas.DataFrame(columns=[self.column_name], data=[4], dtype=numpy.int16)

    @let_now
    def one_column_dataframe_different_column_name(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name_2])

    @let_now
    def two_column_dataframe_no_rows(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2])

    @let_now
    def two_column_dataframe(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2.0]])
    
    @let_now
    def two_column_dataframe_reference_types(self):
        return {self.column_name: 'int64', self.column_name_2: 'float64'}

    @let_now
    def two_column_dataframe_with_datetime(self):
        import pandas
        import datetime
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[
            [datetime.datetime(2020,5,3), datetime.datetime(2021,6,3)],
            [datetime.datetime(2019,7,5), datetime.datetime(2019,6,4)]
        ])

    @let_now
    def two_column_dataframe_different_types(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2]])

    @let_now
    def two_column_dataframe_no_rows_different_second_column(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_3])

    @let_now
    def two_column_dataframe_columns_wrong_order(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name_2, self.column_name])

    @let_now
    def four_column_dataframe_no_rows(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2, self.column_name_3, self.column_name_4])

    @let_now
    def four_column_dataframe_no_rows_different_order(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name_4, self.column_name_2, self.column_name_3, self.column_name])

    @let_now
    def multiple_types_dataframe(self):
        import pandas
        import datetime
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2, self.column_name_3, self.column_name_4], data=[[self.faker.word(), True, self.faker.date_time(), self.faker.pyint()], [self.faker.word(), False, self.faker.date_time(), self.faker.word()]])

    @let_now
    def two_column_dataframe_categories(self):
        return {self.column_name: False, self.column_name_2: False}

    @let_now
    def dataframe_with_strings_and_nans(self):
        import pandas
        import numpy
        return pandas.DataFrame(columns=[self.column_name], data=[self.faker.word() * 10, numpy.nan * 5])

    @let
    def reference_dataframe_with_one_numerical_column(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(i)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.float64)

    @let
    def dataframe_to_validate_with_one_numerical_column(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(12 - i)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.float64)

    def _generate_distinct(self, reference_values, generating_callback):
        candidate_value = generating_callback()
        return candidate_value if candidate_value not in reference_values else self._generate_distinct(reference_values, generating_callback)

    @set_up
    def set_up(self):
        self.mock_file_for_write.__enter__ = lambda *args: self.mock_file_for_write
        self.mock_file_for_write.__exit__ = lambda *args: None

        self.mock_file_for_read.__enter__ = lambda *args: self.mock_file_for_read
        self.mock_file_for_read.__exit__ = lambda *args: None

        self.mock_open.return_when(self.mock_file_for_write, self.data_contract_file_path, 'wb')
        self.mock_open.return_when(self.mock_file_for_read, self.data_contract_file_path, 'rb')

        mock_environ = self.patch('os.environ', {})
        mock_environ['PROJECT_NAME'] = self.project_name
        mock_environ['MONITOR_NAME'] = self.model_name

        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @tear_down
    def tear_down(self):
        self._redis.flushall()

    def test_can_import_data_contract_from_foundations_orbit_top_level(self):
        import foundations_orbit
        self.assertEqual(DataContract, foundations_orbit.DataContract)

    def test_data_contract_takes_contract_name(self):
        try:
            DataContract(self.contract_name, df=self.empty_dataframe)
        except TypeError as ex:
            raise AssertionError('data contract class takes contract name as argument') from ex

    def test_data_contract_has_options_with_default_max_bins_50(self):
        self._test_data_contract_has_default_option('max_bins', 50)
    
    def test_data_contract_has_options_with_default_check_min_max_True(self):
        self._test_data_contract_has_default_option('check_min_max', True)

    def test_data_contract_has_options_with_default_check_row_count_True(self):
        self._test_data_contract_has_default_option('check_row_count', True)

    def test_data_contract_has_options_with_default_special_values_numpy_nan(self):
        import numpy
        self._test_data_contract_has_default_option('special_values', [numpy.nan])

    def test_data_contract_has_options_with_default_check_distribution_True(self):
        self._test_data_contract_has_default_option('check_distribution', True)

    def test_data_contract_has_distribution_option_distance_metric_with_default_value_l_infinity(self):
        self._test_distribution_check_has_default_option('distance_metric', 'l_infinity')

    def test_data_contract_has_distribution_option_default_threshold_0_1(self):
        self._test_distribution_check_has_default_option('default_threshold', 0.1)

    def test_data_contract_has_distribution_option_default_cols_to_include(self):
        self._test_distribution_check_has_default_option('cols_to_include', None)

    def test_data_contract_has_distribution_option_default_cols_to_ignore(self):
        self._test_distribution_check_has_default_option('cols_to_ignore', None)

    def test_data_contract_has_distribution_option_default_custom_thresholds(self):
        self._test_distribution_check_has_default_option('custom_thresholds', {})

    def test_data_contract_can_save_to_file(self):
        import pickle

        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        contract.save(self.monitor_package_directory)

        self.mock_file_for_write.write.assert_called_once_with(pickle.dumps(contract))

    def test_data_contract_save_preserves_options(self):
        import pickle

        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        contract.options = {'asdf': 'value'}

        contract.save(self.monitor_package_directory)

        self.mock_file_for_write.write.assert_called_once_with(pickle.dumps(contract))

    def test_data_contract_has_equality(self):
        self.assertEqual(DataContract(self.contract_name, df=self.empty_dataframe), DataContract(self.contract_name, df=self.empty_dataframe))

    def test_data_contract_with_different_name_is_not_equal(self):
        self.assertNotEqual(DataContract(self.contract_name, df=self.empty_dataframe), DataContract(self.other_contract_name, df=self.empty_dataframe))

    def test_data_contract_with_different_options_are_not_equal(self):
        contract = DataContract(self.contract_name, df=self.empty_dataframe)

        contract_different_options = DataContract(self.contract_name, df=self.empty_dataframe)
        contract_different_options.options = {'whoops': 'hey'}

        self.assertNotEqual(contract, contract_different_options)

    def test_data_contract_load_loads_data_contract_from_file(self):
        import pickle

        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        self.mock_file_for_read.read.return_value = pickle.dumps(contract)

        self.assertEqual(contract, DataContract.load(self.monitor_package_directory, self.contract_name))

    def test_data_contract_load_actually_loads(self):
        import pickle

        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        contract.options = {'some_option': 'with_value'}
        self.mock_file_for_read.read.return_value = pickle.dumps(contract)

        self.assertEqual(contract, DataContract.load(self.monitor_package_directory, self.contract_name))

    def test_data_contract_validate_performs_schema_check_by_default(self):
        mock_schema_check_results = {'passed': True}
        mock_schema_checker_class = self.patch('foundations_orbit.contract_validators.schema_checker.SchemaChecker', ConditionalReturn())
        mock_schema_checker = Mock()

        mock_schema_checker_class.return_when(mock_schema_checker, [self.column_name, self.column_name_2], {self.column_name: 'int64', self.column_name_2: 'float64'})
        mock_schema_checker.validate = ConditionalReturn()
        mock_schema_checker.validate.return_when(mock_schema_check_results, self.two_column_dataframe_no_rows_different_second_column)

        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.options.check_distribution = False
        contract.options.check_special_values = False
        validation_report = contract.validate(self.two_column_dataframe_no_rows_different_second_column, self.datetime_today)
        self.assertEqual(mock_schema_check_results, validation_report['schema_check_results'])
    
    def test_data_contract_validate_excludes_columns_that_failed_from_other_tests(self):
        import pandas, numpy
        reference_dataframe = pandas.DataFrame(columns=[self.column_name, self.column_name_2, self.column_name_3, self.column_name_4, self.column_name_5], 
                                               data=[[1, "string", True, self.faker.date_time(), 1],
                                                     [1, "string", False, self.faker.date_time(), "string"]])
        current_dataframe = pandas.DataFrame(columns=[self.column_name, self.column_name_2, self.column_name_3, self.column_name_4, self.column_name_5],
                                               data=[[1, self.faker.pyfloat(), self.faker.word(), self.faker.pyint(), self.faker.word()],
                                                     [1, self.faker.pyfloat(), self.faker.word(), self.faker.pyint(), self.faker.word()]])

        contract = DataContract(self.contract_name, df=reference_dataframe)
        contract.special_value_test.configure(attributes=list(current_dataframe.columns)[:-1], thresholds={numpy.nan: 0.1})
        contract.min_max_test.configure(attributes=[list(current_dataframe.columns)[0]], lower_bound=0, upper_bound=2)
        validation_report = contract.validate(current_dataframe, self.datetime_today)

        del validation_report['metadata']
        del validation_report['min_max_test_results']
        del validation_report['row_count']
        del validation_report['schema_check_results']
        for test_dict in validation_report.values():
            cols_to_ignore = {self.column_name_2, self.column_name_3, self.column_name_4}
            self.assertTrue(cols_to_ignore.issubset(set(test_dict.keys())))
            for ignored_col in cols_to_ignore:
                self.assertEqual("Schema Test Failed", test_dict[ignored_col]['message'])

    def test_data_contract_exclude_calls_exclude_of_all_tests_for_single_column(self):
        distribution_checker_exclude = self.patch('foundations_orbit.contract_validators.distribution_checker.DistributionChecker.exclude')
        min_max_checker_exclude = self.patch('foundations_orbit.contract_validators.min_max_checker.MinMaxChecker.exclude')
        special_values_checker_exclude = self.patch('foundations_orbit.contract_validators.special_values_checker.SpecialValuesChecker.exclude')

        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        contract.exclude(self.column_name)

        distribution_checker_exclude.assert_called_once()
        min_max_checker_exclude.assert_called_once()
        special_values_checker_exclude.assert_called_once()
    
    def test_data_contract_exclude_calls_exclude_of_all_tests_for_one_of_multiple_columns(self):
        distribution_checker_exclude = self.patch('foundations_orbit.contract_validators.distribution_checker.DistributionChecker.exclude')
        min_max_checker_exclude = self.patch('foundations_orbit.contract_validators.min_max_checker.MinMaxChecker.exclude')
        special_values_checker_exclude = self.patch('foundations_orbit.contract_validators.special_values_checker.SpecialValuesChecker.exclude')

        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.exclude([self.column_name, self.column_name_2])

        distribution_checker_exclude.assert_called_once()
        min_max_checker_exclude.assert_called_once()
        special_values_checker_exclude.assert_called_once()

    def test_data_contract_validate_check_distributions_by_default(self):

        mock_report_validator = self.patch('foundations_orbit.report_formatter.ReportFormatter')
        mock_bin_create_stats = self.patch('foundations_orbit.contract_validators.utils.create_bin_stats.create_bin_stats')
        mock_bin_create_stats.return_value = self.bin_return_value
        mock_distribution_checker = Mock()
        mock_distribution_check_results = Mock()

        contract = DataContract(self.contract_name, df=self.two_column_dataframe)

        self.patch('foundations_orbit.contract_validators.special_values_checker.SpecialValuesChecker')
        mock_distribution_checker_class = self.patch('foundations_orbit.contract_validators.distribution_checker.DistributionChecker', ConditionalReturn())
        mock_distribution_checker_class.return_when(mock_distribution_checker, contract.options.distribution, self.bin_stats, [self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, self.two_column_dataframe_categories)

        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        
        mock_distribution_checker.validate = ConditionalReturn()
        mock_distribution_checker.validate.return_when(mock_distribution_check_results, self.two_column_dataframe)

        validation_report = contract.validate(self.two_column_dataframe)

        self.assertEqual(mock_distribution_check_results, validation_report['dist_check_results'])

    def test_data_contract_validate_does_not_check_distribution_if_option_set_to_false(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.options.check_distribution = False

        self.assertNotIn('dist_check_results', contract.validate(self.two_column_dataframe))

    def test_data_contract_validate_checks_row_count_by_default(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        self.assertIn('row_count', contract.validate(self.two_column_dataframe))

    def test_data_contract_validate_number_of_rows_if_option_set(self):
        mock_row_count_check_results = self.row_count_results
        mock_row_count_checker_class = self.patch('foundations_orbit.contract_validators.row_count_checker.RowCountChecker', ConditionalReturn())
        mock_row_count_checker = Mock()

        mock_row_count_checker_class.return_when(mock_row_count_checker, 1)
        mock_row_count_checker.validate = ConditionalReturn()
        mock_row_count_checker.validate.return_when(mock_row_count_check_results, self.one_column_dataframe)

        contract = self._contract_from_dataframe_for_row_checking(self.one_column_dataframe)
        validation_report = contract.validate(self.one_column_dataframe)

        self.assertEqual(mock_row_count_check_results, validation_report['row_count'])

    def test_data_contract_validation_report_has_metadata_for_reference_and_current_dataframe(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        report = contract.validate(self.two_column_dataframe_different_types)

        expected_metadata = {
            'reference_metadata': {
                'column_names': [
                    self.column_name, 
                    self.column_name_2
                ],
                'type_mapping': {
                    self.column_name: 'int64', 
                    self.column_name_2: 'float64'
                },
            },
            'current_metadata': {
                'column_names': [
                    self.column_name, 
                    self.column_name_2
                ],
                'type_mapping': {
                    self.column_name: 'int64', 
                    self.column_name_2: 'int64'
                }
            }
        }

        self.assertEqual(expected_metadata, report['metadata'])

    def test_data_contract_validate_writes_correct_info_to_redis(self):
        import numpy

        self.maxDiff = None
        inference_period=self.inference_period
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.special_value_test.configure(attributes=[self.column_name, self.column_name_2], thresholds={numpy.nan: 0.1})
        contract.min_max_test.configure(attributes=[self.column_name, self.column_name_2], lower_bound=0, upper_bound=1)
        report = contract.validate(self.two_column_dataframe_different_types, inference_period=inference_period)

        expected_output = {
            'attribute_names': list(self.two_column_dataframe.columns),
            'data_contract': f'{self.contract_name}',
            'data_quality': {
                'details_by_attribute': [{
                        'attribute_name': f'{self.column_name}',
                        'difference_in_pct': 0.0,
                        'pct_in_current_data': 0.0,
                        'pct_in_reference_data': 0.0,
                        'validation_outcome': 'healthy',
                        'value': 'nan'
                    }
                ],
                'summary': {
                    'critical': 0,
                    'healthy': 1,
                    'warning': 0
                }
            },
            'date': f'{inference_period}',
            'monitor_package': f'{self.model_name}',
            'population_shift': {
                'details_by_attribute': [{
                        'L-infinity': 0.0,
                        'attribute_name': f'{self.column_name}',
                        'validation_outcome': 'healthy'
                    }
                ],
                'summary': {
                    'critical': 0,
                    'healthy': 1,
                    'warning': 0
                }
            },
            'row_count': {
                'expected_row_count': len(self.two_column_dataframe),
                'actual_row_count': len(self.two_column_dataframe_different_types),
                'row_count_diff': (len(self.two_column_dataframe_different_types) - len(self.two_column_dataframe)) / len(self.two_column_dataframe)
            },
            'schema': {
                'details_by_attribute': [{
                    'attribute_name': f'{self.column_name_2}',
                    'data_type': 'int64',
                    'issue_type': 'datatype in reference dataframe is float64',
                    'validation_outcome': 'critical'
                }],
                'summary': {
                    'critical': 1,
                    'healthy': 1,
                    'warning': 0
                }
            },
            'min': {
                'details_by_attribute': [{
                    'attribute_name': f'{self.column_name}',
                    'lower_bound': 0,
                    'min_value': 1,
                    'validation_outcome': 'healthy',
                }],
                'summary': {
                    'critical': 0,
                    'healthy': 1,
                    'warning': 0
                }
            },
            'max': {
                'details_by_attribute': [{
                    'attribute_name': f'{self.column_name}',
                    'upper_bound': 1,
                    'max_value': 1,
                    'validation_outcome': 'healthy',
                }],
                'summary': {
                    'critical': 0,
                    'healthy': 1,
                    'warning': 0
                }
            }
        }

        key = f'projects:{self.project_name}:monitors:{self.model_name}:validation:{self.contract_name}'
        serialized_report = self._redis.hget(key, inference_period)
        validation_counter = self._redis.get(f'{key}:counter')

        self.assertEqual(1, int(validation_counter.decode()))

        import pickle
        deserialized_report = pickle.loads(serialized_report)

        self.assertIn('user', deserialized_report)
        del deserialized_report['user']
        self.assertIn('job_id', deserialized_report)
        del deserialized_report['job_id']

        self.assertEqual(expected_output, deserialized_report)

    def test_data_contract_validate_writes_correct_info_to_redis_using_datetime(self):
        import numpy
        import datetime

        self.maxDiff = None

        inference_period=self.inference_period
        contract = DataContract(self.contract_name, df=self.two_column_dataframe_with_datetime)
        contract.special_value_test.configure(attributes=[self.column_name, self.column_name_2], thresholds={numpy.nan: 0.1})

        upper_bound = datetime.datetime(2023,5,6)

        contract.min_max_test.configure(attributes=[self.column_name], lower_bound=datetime.datetime(2016,2,6), upper_bound=upper_bound)
        contract.min_max_test.configure(attributes=[self.column_name_2], lower_bound=datetime.datetime(2020,2,6), upper_bound=upper_bound)

        contract.options.check_distribution = False
        contract.options.check_special_values = False
        report = contract.validate(self.two_column_dataframe_with_datetime, inference_period=inference_period)

        expected_output = {
            'attribute_names': list(self.two_column_dataframe_with_datetime.columns),
            'data_contract': f'{self.contract_name}',
            'date': f'{inference_period}',
            'data_quality': {},
            'monitor_package': f'{self.model_name}',
            'min': {
                'details_by_attribute': [{
                    'attribute_name': f'{self.column_name}',
                    'lower_bound': datetime.datetime(2016,2,6),
                    'min_value': self.two_column_dataframe_with_datetime[self.column_name].min(),
                    'validation_outcome': 'healthy',
                },
                {
                    'attribute_name': f'{self.column_name_2}',
                    'lower_bound': datetime.datetime(2020,2,6),
                    'min_value': self.two_column_dataframe_with_datetime[self.column_name_2].min(),
                    'validation_outcome': 'critical',
                    'percentage_out_of_bounds': 0.5,
                }],
                'summary': {
                    'critical': 1,
                    'healthy': 1,
                    'warning': 0
                }
            },
            'max': {
                'details_by_attribute': [{
                    'attribute_name': f'{self.column_name}',
                    'upper_bound': upper_bound,
                    'max_value': self.two_column_dataframe_with_datetime[self.column_name].max(),
                    'validation_outcome': 'healthy',
                },
                {
                    'attribute_name': f'{self.column_name_2}',
                    'upper_bound': upper_bound,
                    'max_value': self.two_column_dataframe_with_datetime[self.column_name_2].max(),
                    'validation_outcome': 'healthy',
                }],
                'summary': {
                    'critical': 0,
                    'healthy': 2,
                    'warning': 0
                }
            },
            'population_shift': {},
            'row_count': {
                'expected_row_count': len(self.two_column_dataframe_with_datetime),
                'actual_row_count': len(self.two_column_dataframe_with_datetime),
                'row_count_diff': 0.0
            }
        }

        key = f'projects:{self.project_name}:monitors:{self.model_name}:validation:{self.contract_name}'
        serialized_report = self._redis.hget(key, inference_period)
        validation_counter = self._redis.get(f'{key}:counter')

        self.assertEqual(1, int(validation_counter.decode()))

        import pickle
        deserialized_report = pickle.loads(serialized_report)

        deserialized_report.pop('schema', None)

        self.assertIn('user', deserialized_report)
        del deserialized_report['user']
        self.assertIn('job_id', deserialized_report)
        del deserialized_report['job_id']

        self.assertEqual(expected_output, deserialized_report)

    def test_data_contract_validate_writes_correct_summary_info_to_redis(self):
        import pickle

        inference_period = self.inference_period
        contract = DataContract(self.contract_name, df=self.reference_dataframe_with_one_numerical_column)
        contract.validate(self.dataframe_to_validate_with_one_numerical_column, inference_period=inference_period)

        expected_output = {
            'attribute_summaries': {
                'feat_1': {
                    'expected_data_summary': {
                        'percentage_missing': 0.0,
                        'minimum': 1.0,
                        'maximum': 11.0
                    },
                    'actual_data_summary': {
                        'percentage_missing': 0.0,
                        'minimum': 1.0,
                        'maximum': 11.0
                    },
                    'binned_data': {
                        'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                                 '9.0-10.0', '10.0-11.0'],
                        'data': {
                            'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21],
                            'actual_data': [11, 10, 9, 8, 7, 6, 5, 4, 3, 3]
                        }
                    }
                }
            },
            'num_critical_tests': 1
        }

        key = f'projects:{self.project_name}:monitors:{self.model_name}:validation:{self.contract_name}:summary'
        serialized_report = self._redis.hget(key, inference_period)
        deserialized_report = pickle.loads(serialized_report)

        self.maxDiff = None
        self.assertEqual(expected_output, deserialized_report)

    def test_data_contract_distribution_check_produces_correct_output_for_two_column_df_different_types(self):
        inference_period=self.inference_period
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        report = contract.validate(self.two_column_dataframe_different_types, inference_period=inference_period)
        dist_check_results = report['dist_check_results']
        import numpy as np

        expected_results = {
            self.column_name: {
                'binned_l_infinity': 0.0,
                'binned_passed': True
            },
            self.column_name_2: {
                'binned_passed': False,
                'message': 'Schema Test Failed'
            }
        }

        self.assertEqual(expected_results, dist_check_results)
    
    def test_data_contract_has_schema_checker(self):
        self._test_data_contract_has_test_as_attribute('schema_test')
    
    def test_data_contract_has_special_values_checker(self):
        self._test_data_contract_has_test_as_attribute('special_value_test')
    
    def test_data_contract_has_distribution_checker(self):
        self._test_data_contract_has_test_as_attribute('distribution_test')
    
    def test_data_contract_has_min_max_checker(self):
        self._test_data_contract_has_test_as_attribute('min_max_test')

    def test_data_contract_has_summary(self):
        self._test_data_contract_has_test_as_attribute('summary')
    
    def test_data_contract_has_schema_checker_configured(self):
        from foundations_orbit.contract_validators.schema_checker import SchemaChecker
        self._test_data_contract_has_test_which_is_an_instance_of_expected_class('schema_test', SchemaChecker)
    
    def test_data_contract_has_special_values_test_configured(self):
        from foundations_orbit.contract_validators.special_values_checker import SpecialValuesChecker
        self._test_data_contract_has_test_which_is_an_instance_of_expected_class('special_value_test', SpecialValuesChecker)
    
    def test_data_contract_has_distribution_test_configured(self):
        from foundations_orbit.contract_validators.distribution_checker import DistributionChecker
        self._test_data_contract_has_test_which_is_an_instance_of_expected_class('distribution_test', DistributionChecker)
    
    def test_data_contract_has_min_max_test_configured(self):
        from foundations_orbit.contract_validators.min_max_checker import MinMaxChecker
        self._test_data_contract_has_test_which_is_an_instance_of_expected_class('min_max_test', MinMaxChecker)
    
    def test_data_contract_validate_min_max_test_if_option_set(self):
        mock_min_max_checker_class = self.patch('foundations_orbit.contract_validators.min_max_checker.MinMaxChecker.validate')

        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.validate(self.two_column_dataframe)
        mock_min_max_checker_class.assert_called_once()
    
    def test_data_contract_min_max_check_produces_correct_output_for_two_column_df(self):
        inference_period=self.inference_period
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.min_max_test.configure(attributes=[self.column_name], lower_bound=0, upper_bound=100)
        report = contract.validate(self.one_column_dataframe_four_rows, inference_period=inference_period)

        self.assertIn('min_max_test_results', report)

        min_max_test_results = report['min_max_test_results']

        import numpy as np

        expected_results = {
            self.column_name: {
                'min_test': {
                    'lower_bound': 0,
                    'passed': True,
                    'min_value': 4
                },
                'max_test': {
                    'upper_bound': 100,
                    'passed': True,
                    'max_value': 7
                }
            }
        }

        self.assertEqual(expected_results, min_max_test_results)
    
    def test_data_contract_min_max_check_produces_correct_output_for_two_column_df_with_datetime(self):
        import datetime

        inference_period=self.inference_period
        contract = DataContract(self.contract_name, df=self.two_column_dataframe_with_datetime)

        upper_bound = datetime.datetime(2023,5,6)

        contract.min_max_test.configure(attributes=[self.column_name], lower_bound=datetime.datetime(2016,2,6), upper_bound=upper_bound)
        contract.min_max_test.configure(attributes=[self.column_name_2], lower_bound=datetime.datetime(2020,2,6), upper_bound=upper_bound)
        contract.options.check_distribution = False
        contract.options.check_special_values = False

        report = contract.validate(self.two_column_dataframe_with_datetime, inference_period=inference_period)

        self.assertIn('min_max_test_results', report)

        min_max_test_results = report['min_max_test_results']

        expected_results = {
            self.column_name: {
                'min_test': {
                    'lower_bound': datetime.datetime(2016,2,6),
                    'passed': True,
                    'min_value': self.two_column_dataframe_with_datetime[self.column_name].min()
                },
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': self.two_column_dataframe_with_datetime[self.column_name].max()
                }
            },
            self.column_name_2: {
                'min_test': {
                    'lower_bound': datetime.datetime(2020,2,6),
                    'passed': False,
                    'min_value': self.two_column_dataframe_with_datetime[self.column_name_2].min(),
                    'percentage_out_of_bounds': 0.5
                },
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': self.two_column_dataframe_with_datetime[self.column_name_2].max()
                }
            }
        }

        self.assertEqual(expected_results, min_max_test_results)

    def test_data_contract_does_not_run_min_max_test_when_options_configured(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.options.check_min_max = False

        self.assertNotIn('min_max_test_results', contract.validate(self.two_column_dataframe))

    @skip# @quarantine
    def test_data_contract_distribution_check_produces_correct_output_for_two_column_df_no_rows_different_second_column(self):
        inference_period=self.inference_period
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        report = contract.validate(self.two_column_dataframe_no_rows_different_second_column, inference_period=inference_period)
        dist_check_results = report['dist_check_results']
        import numpy as np

        expected_results = {
            self.column_name: {
                'special_values': {
                    np.nan: {
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0,
                        'current_percentage': 0.0,
                        'passed': True
                    }
                },
                'binned_l_infinity': 0.0,
                'binned_passed': True
            },
            self.column_name_3: {
                'special_values': {
                    np.nan: {
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0,
                        'current_percentage': 0.0,
                        'passed': False
                    }
                },
                'binned_l_infinity': 0.0,
                'binned_passed': False
            }
        }

        self.assertEqual(expected_results, dist_check_results)

    def test_special_values_checker_for_datetime_input_returns_expected_result(self):
        import numpy
        data = {
            self.column_name: [self.faker.date_time(), self.faker.date_time(), self.faker.date_time()] + [numpy.nan],
            self.column_name_2: [self.faker.date_time(), self.faker.date_time(), self.faker.date_time()] + [numpy.nan]
        }

        self._test_special_values_checker_for_datatype_input_returns_expected_results(data)

    def test_special_values_checker_for_string_input_returns_expected_result(self):
        self.maxDiff = None
        import numpy
        data = {
            self.column_name: [self.faker.word()]*3 + [numpy.nan],
            self.column_name_2: [self.faker.word()]*3 + [numpy.nan]
        }

        self._test_special_values_checker_for_datatype_input_returns_expected_results(data)

    def test_special_values_checker_for_bool_input_returns_expected_result(self):
        import numpy
        data = {
            self.column_name: [True, False, False] + [numpy.nan],
            self.column_name_2: [True, True, True] + [numpy.nan]
        }

        self._test_special_values_checker_for_datatype_input_returns_expected_results(data)

    def test_data_contract_with_no_reference_dataframe_throws_error(self):
        with self.assertRaises(ValueError) as exception:
            contract = DataContract(self.contract_name)

    def test_dataframe_statistics_returns_string_column_type_when_column_contains_strings_and_nans_only(self):
        from foundations_orbit.utils.dataframe_statistics import dataframe_statistics
        _,column_types,_ = dataframe_statistics(self.dataframe_with_strings_and_nans)
        self.assertEqual('str', column_types[self.column_name])

    def test_data_contract_to_string_prints_expected_output(self):
        import numpy, json
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.min_max_test.configure(attributes=[self.column_name, self.column_name_2], lower_bound = 0, upper_bound = 100)
        contract.special_value_test.configure(attributes=[self.column_name], thresholds={numpy.nan: 0.5})
        contract.special_value_test.configure(attributes=[self.column_name_2], thresholds={60: 0.5, numpy.nan: 0.1})

        result = str(contract)

        # import json
        # print(json.loads(result.replace('\'', '"')))

        tests = ['special_values_test', 'min_max_test', 'distribution_test', 'schema_test']
        for test in tests:
            if test not in result:
                self.fail()

    def _test_special_values_checker_for_datatype_input_returns_expected_results(self, data):
        import pandas, numpy
        dataframe = pandas.DataFrame(data)
        data_contract = DataContract(self.contract_name, dataframe)

        expected_results = {
            self.column_name: {
                numpy.nan: {
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.25,
                    'passed': True
                }
                
            },
            self.column_name_2: {
                numpy.nan: {
                    'percentage_diff': 0.25,
                    'ref_percentage': 0.25,
                    'current_percentage': 0.50,
                    'passed': False
                }
            }
        }

        data_contract.special_value_test.configure(attributes=[self.column_name, self.column_name_2], thresholds={numpy.nan: 0.1})
        dataframe_to_validate = dataframe.copy()
        dataframe_to_validate.iloc[0,1] = numpy.nan
        results = data_contract.validate(dataframe_to_validate)['special_values_check_results']

        self.assertEqual(expected_results, results)

    def _find_if_key_in_dictionary(self, dictionary_to_search, key):
        if key in dictionary_to_search: return True
        for _, value in dictionary_to_search.items():
            if isinstance(value,dict):
                return self._find_if_key_in_dictionary(value, key)

    def _test_data_contract_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        self.assertEqual(default_value, getattr(contract.options, option_name))

    def _test_distribution_check_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        self.assertEqual(default_value, contract.options.distribution[option_name])

    def _contract_from_dataframe_for_row_checking(self, dataframe):
        contract = DataContract(self.contract_name, df=dataframe)
        contract.options.check_row_count = True
        contract.options.check_distribution = False

        return contract
    
    def _test_data_contract_has_test_as_attribute(self, test_name):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        self.assertIsNotNone(getattr(contract, test_name, None))
    
    def _test_data_contract_has_test_which_is_an_instance_of_expected_class(self, test_name, class_type):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        self.assertIsInstance(getattr(contract, test_name, None), class_type)