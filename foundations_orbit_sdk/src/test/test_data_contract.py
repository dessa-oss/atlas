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
    def model_package_directory(self):
        return self.faker.file_path()

    @let
    def data_contract_file_path(self):
        return f'{self.model_package_directory}/{self.contract_name}.pkl'

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
    def row_count_results(self):
        return self.faker.random.random()

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
        mock_environ['MODEL_NAME'] = self.model_name

        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @tear_down
    def tear_down(self):
        self._redis.flushall()

    def test_can_import_data_contract_from_foundations_orbit_top_level(self):
        import foundations_orbit
        self.assertEqual(DataContract, foundations_orbit.DataContract)

    def test_data_contract_takes_contract_name(self):
        try:
            DataContract(self.contract_name)
        except TypeError as ex:
            raise AssertionError('data contract class takes contract name as argument') from ex

    def test_data_contract_has_options_with_default_max_bins_50(self):
        self._test_data_contract_has_default_option('max_bins', 50)

    def test_data_contract_has_options_with_default_check_row_count_False(self):
        self._test_data_contract_has_default_option('check_row_count', False)

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

        contract = DataContract(self.contract_name)
        contract.save(self.model_package_directory)

        self.mock_file_for_write.write.assert_called_once_with(pickle.dumps(contract))

    def test_data_contract_save_preserves_options(self):
        import pickle

        contract = DataContract(self.contract_name)
        contract.options = {'asdf': 'value'}

        contract.save(self.model_package_directory)

        self.mock_file_for_write.write.assert_called_once_with(pickle.dumps(contract))

    def test_data_contract_has_equality(self):
        self.assertEqual(DataContract(self.contract_name), DataContract(self.contract_name))

    def test_data_contract_with_different_name_is_not_equal(self):
        self.assertNotEqual(DataContract(self.contract_name), DataContract(self.other_contract_name))

    def test_data_contract_with_different_options_are_not_equal(self):
        contract = DataContract(self.contract_name)

        contract_different_options = DataContract(self.contract_name)
        contract_different_options.options = {'whoops': 'hey'}

        self.assertNotEqual(contract, contract_different_options)

    def test_data_contract_load_loads_data_contract_from_file(self):
        import pickle

        contract = DataContract(self.contract_name)
        self.mock_file_for_read.read.return_value = pickle.dumps(contract)

        self.assertEqual(contract, DataContract.load(self.model_package_directory, self.contract_name))

    def test_data_contract_load_actually_loads(self):
        import pickle

        contract = DataContract(self.contract_name)
        contract.options = {'some_option': 'with_value'}
        self.mock_file_for_read.read.return_value = pickle.dumps(contract)

        self.assertEqual(contract, DataContract.load(self.model_package_directory, self.contract_name))

    def test_data_contract_validate_performs_schema_check_by_default(self):
        mock_schema_check_results = {'passed': True}
        mock_schema_checker_class = self.patch('foundations_orbit.contract_validators.schema_checker.SchemaChecker', ConditionalReturn())
        mock_schema_checker = Mock()

        mock_schema_checker_class.return_when(mock_schema_checker, [self.column_name, self.column_name_2], {self.column_name: 'int64', self.column_name_2: 'float64'})
        mock_schema_checker.schema_check_results = ConditionalReturn()
        mock_schema_checker.schema_check_results.return_when(mock_schema_check_results, [self.column_name, self.column_name_3], {self.column_name: 'object', self.column_name_3: 'object'})

        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.options.check_distribution = False
        validation_report = contract.validate(self.two_column_dataframe_no_rows_different_second_column, self.datetime_today)
        self.assertEqual(mock_schema_check_results, validation_report['schema_check_results'])

    @skip('PLEASE PUT ME BACK IN WHEN REMOVING PROTOTYPE CODE')
    def test_data_contract_validate_check_distributions_by_default(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)

        mock_distribution_check_results = Mock()
        mock_distribution_checker_class = self.patch('foundations_orbit.contract_validators.distribution_checker.DistributionChecker', ConditionalReturn())
        mock_distribution_checker = Mock()

        mock_distribution_checker_class.return_when(mock_distribution_checker, contract.options.distribution)
        mock_distribution_checker.distribution_check_results = ConditionalReturn()
        mock_distribution_checker.distribution_check_results.return_when(mock_distribution_check_results, [self.column_name, self.column_name_2])

        validation_report = contract.validate(self.two_column_dataframe)

        self.assertEqual(mock_distribution_check_results, validation_report['dist_check_results'])

    def test_data_contract_validate_does_not_check_distribution_if_option_set_to_false(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.options.check_distribution = False

        self.assertNotIn('dist_check_results', contract.validate(self.two_column_dataframe))

    def test_data_contract_validate_does_not_check_row_count_by_default(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        self.assertNotIn('row_cnt_diff', contract.validate(self.two_column_dataframe))

    def test_data_contract_validate_number_of_rows_if_option_set(self):
        mock_row_count_check_results = self.row_count_results
        mock_row_count_checker_class = self.patch('foundations_orbit.contract_validators.row_count_checker.RowCountChecker', ConditionalReturn())
        mock_row_count_checker = Mock()

        mock_row_count_checker_class.return_when(mock_row_count_checker, 1)
        mock_row_count_checker.row_count_difference = ConditionalReturn()
        mock_row_count_checker.row_count_difference.return_when(mock_row_count_check_results, 1)

        contract = self._contract_from_dataframe_for_row_checking(self.one_column_dataframe)
        validation_report = contract.validate(self.one_column_dataframe)

        self.assertEqual(mock_row_count_check_results, validation_report['row_cnt_diff'])

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
        self.maxDiff = None
        inference_period='2019-09-17'
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        report = contract.validate(self.two_column_dataframe_different_types, inference_period=inference_period)

        expected_output = {
            'data_contract': f'{self.contract_name}',
            'data_quality': {
                'details_by_attribute': [{
                        'attribute_name': f'{self.column_name}',
                        'difference_in_pct': 0.0,
                        'pct_in_current_data': 0.0,
                        'pct_in_reference_data': 0.0,
                        'validation_outcome': 'healthy',
                        'value': 'nan'
                    },
                    {
                        'attribute_name': f'{self.column_name_2}',
                        'difference_in_pct': 0.0,
                        'pct_in_current_data': 0.0,
                        'pct_in_reference_data': 0.0,
                        'validation_outcome': 'healthy',
                        'value': 'nan'
                    }
                ],
                'summary': {
                    'critical': 0,
                    'healthy': 2
                }
            },
            'date': f'{inference_period}',
            'details_by_attribute': [{
                'attribute_name': f'{self.column_name_2}',
                'data_type': 'int64',
                'issue_type': 'datatype in reference is float64',
                'validation_outcome': 'error_state'
            }],
            'model_package': f'{self.model_name}',
            'population_shift': {
                'details_by_attribute': [{
                        'L-infinity': 0.0,
                        'attribute_name': f'{self.column_name}',
                        'validation_outcome': 'healthy'
                    },
                    {
                        'L-infinity': 0.0,
                        'attribute_name': f'{self.column_name_2}',
                        'validation_outcome': 'healthy'
                    }
                ],
                'summary': {
                    'critical': 0,
                    'healthy': 2
                }
            },
            'row_cnt_diff': 0,
            'schema': {
                'summary': {
                    'critical': 1,
                    'healthy': 1
                }
            }
        }

        key = f'projects:{self.project_name}:models:{self.model_name}:validation:{self.contract_name}'
        serialized_report = self._redis.hget(key, inference_period)
        import pickle
        deserialized_report = pickle.loads(serialized_report)

        self.assertEqual(expected_output, deserialized_report)


    def _test_data_contract_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name)
        self.assertEqual(default_value, getattr(contract.options, option_name))

    def _test_distribution_check_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name)
        self.assertEqual(default_value, contract.options.distribution[option_name])

    def _contract_from_dataframe_for_row_checking(self, dataframe):
        contract = DataContract(self.contract_name, df=dataframe)
        contract.options.check_row_count = True
        contract.options.check_distribution = False

        return contract