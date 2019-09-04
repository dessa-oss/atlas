"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

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

    def test_data_contract_has_options_with_default_check_schema_True(self):
        self._test_data_contract_has_default_option('check_schema', True)

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

    def test_data_contract_validate_empty_dataframe_against_itself_passes_schema_check(self):
        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        validation_report = contract.validate(self.empty_dataframe, self.datetime_today)
        self.assertEqual({'passed': True}, validation_report['schema_check_results'])

    def test_data_contract_validate_empty_dataframe_against_itself_returns_empty_dist_check_results(self):
        contract = DataContract(self.contract_name, df=self.empty_dataframe)
        validation_report = contract.validate(self.empty_dataframe, self.datetime_today)
        self.assertEqual({}, validation_report['dist_check_results'])

    def test_data_contract_validate_single_column_dataframe_against_itself_returns_dist_check_result_with_one_entry(self):
        import numpy

        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        validation_report = contract.validate(self.one_column_dataframe, self.datetime_today)

        expected_dist_check_result = {
            self.column_name: {
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
        }

        self.assertEqual(expected_dist_check_result, validation_report['dist_check_results'])

    def test_data_contract_validate_multiple_column_dataframe_against_itself_returns_dist_check_result_with_multiple_entries(self):
        import numpy

        self.maxDiff = None

        contract = DataContract(self.contract_name, df=self.two_column_dataframe_no_rows)
        validation_report = contract.validate(self.two_column_dataframe_no_rows, self.datetime_today)

        expected_dist_check_result = {
            self.column_name: {
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
            },
            self.column_name_2: {
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
        }

        self.assertEqual(expected_dist_check_result, validation_report['dist_check_results'])

    def test_data_contract_validate_dataframe_with_zero_columns_against_dataframe_with_one_column_fails_schema_check(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        validation_report = contract.validate(self.empty_dataframe, self.datetime_today)

        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [],
            'missing_in_current': [self.column_name]
        }

        self.assertEqual(expected_schema_check_results, validation_report['schema_check_results'])

    def test_data_contract_validate_dataframe_with_one_column_against_another_dataframe_with_one_column_but_different_name_fails_schema_check(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        validation_report = contract.validate(self.one_column_dataframe_different_column_name, self.datetime_today)

        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [self.column_name_2],
            'missing_in_current': [self.column_name]
        }

        self.assertEqual(expected_schema_check_results, validation_report['schema_check_results'])

    def test_data_contract_validate_dataframe_with_one_column_against_another_dataframe_with_two_columns_first_column_the_same_fails_schema_check(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        validation_report = contract.validate(self.two_column_dataframe_no_rows, self.datetime_today)

        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [self.column_name_2],
            'missing_in_current': []
        }

        self.assertEqual(expected_schema_check_results, validation_report['schema_check_results'])

    def test_data_contract_validate_dataframe_with_one_column_against_itself_passes_schema_check(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        validation_report = contract.validate(self.one_column_dataframe, self.datetime_today)
        self.assertEqual({'passed': True}, validation_report['schema_check_results'])

    def test_data_contract_validate_dataframe_with_multiple_columns_against_itself_passes_schema_check(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe_no_rows)
        validation_report = contract.validate(self.two_column_dataframe_no_rows, self.datetime_today)
        self.assertEqual({'passed': True}, validation_report['schema_check_results'])

    def test_data_contract_validate_dataframe_with_two_columns_against_different_dataframe_with_two_columns_fails_schema_check(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe_no_rows)
        validation_report = contract.validate(self.two_column_dataframe_no_rows_different_second_column, self.datetime_today)

        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [self.column_name_3],
            'missing_in_current': [self.column_name_2]
        }

        self.assertEqual(expected_schema_check_results, validation_report['schema_check_results'])

    def test_data_contract_validate_does_not_perform_schema_check_if_check_schema_option_is_false(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe_no_rows)
        contract.options.check_schema = False
        validation_report = contract.validate(self.two_column_dataframe_no_rows_different_second_column, self.datetime_today)
        self.assertNotIn('schema_check_results', validation_report)

    def test_data_contract_validate_column_names_wrong_order_fails_schema_check(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe_no_rows)
        validation_report = contract.validate(self.two_column_dataframe_columns_wrong_order)

        expected_schema_check_results = {
            'passed': False,
            'error_message': 'columns not in order',
            'columns_out_of_order': [self.column_name_2, self.column_name]
        }

        self.assertEqual(expected_schema_check_results, validation_report['schema_check_results'])

    def test_data_contract_validate_column_names_wrong_order_fails_schema_check_more_rows(self):
        contract = DataContract(self.contract_name, df=self.four_column_dataframe_no_rows)
        validation_report = contract.validate(self.four_column_dataframe_no_rows_different_order)

        expected_schema_check_results = {
            'passed': False,
            'error_message': 'columns not in order',
            'columns_out_of_order': [self.column_name_4, self.column_name]
        }

        self.assertEqual(expected_schema_check_results, validation_report['schema_check_results'])

    def test_data_contract_validate_single_column_dataframe_column_types_fails_when_column_type_does_not_match(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        validation_report = contract.validate(self.one_column_dataframe_different_data_type)

        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column datatype mismatches',
            'cols': {
                self.column_name: {
                    'ref_type': 'int8',
                    'current_type': 'int16'
                }
            }
        }

        self.assertEqual(expected_schema_check_results, validation_report['schema_check_results'])

    def test_data_contract_validate_two_column_dataframe_column_types_fails_when_column_type_does_not_match(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        validation_report = contract.validate(self.two_column_dataframe_different_types)

        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column datatype mismatches',
            'cols': {
                self.column_name_2: {
                    'ref_type': 'float64',
                    'current_type': 'int64'
                }
            }
        }

        self.assertEqual(expected_schema_check_results, validation_report['schema_check_results'])

    def test_data_contract_validate_does_not_check_distribution_if_option_set_to_false(self):
        contract = DataContract(self.contract_name, df=self.two_column_dataframe)
        contract.options.check_distribution = False

        self.assertNotIn('dist_check_results', contract.validate(self.two_column_dataframe))

    def test_data_contract_validate_number_of_rows_if_option_set(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        contract.options.check_row_count = True
        contract.options.check_distribution = False
        validation_report = contract.validate(self.one_column_dataframe)

        expected_validation_report = {
            'schema_check_results': {'passed': True},
            'row_cnt_diff': 0.0
        }

        self.assertEqual(expected_validation_report, validation_report)

    def test_data_contract_validate_number_of_rows_different_dataframe_lengths(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        contract.options.check_row_count = True
        contract.options.check_distribution = False
        validation_report = contract.validate(self.one_column_dataframe_two_rows)

        expected_validation_report = {
            'schema_check_results': {'passed': True},
            'row_cnt_diff': 1.0
        }

        self.assertEqual(expected_validation_report, validation_report)

    def test_data_contract_validate_number_of_rows_different_dataframe_lengths_again(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        contract.options.check_row_count = True
        contract.options.check_distribution = False
        validation_report = contract.validate(self.one_column_dataframe_four_rows)

        expected_validation_report = {
            'schema_check_results': {'passed': True},
            'row_cnt_diff': 3.0
        }

        self.assertEqual(expected_validation_report, validation_report)

    def test_data_contract_validate_number_of_rows_different_dataframe_lengths_again_again(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe_two_rows)
        contract.options.check_row_count = True
        contract.options.check_distribution = False
        validation_report = contract.validate(self.one_column_dataframe)

        expected_validation_report = {
            'schema_check_results': {'passed': True},
            'row_cnt_diff': 0.5
        }

        self.assertEqual(expected_validation_report, validation_report)

    def test_data_contract_cannot_validate_if_checking_distribution_if_both_column_whitelist_and_column_blacklist_are_set(self):
        contract = DataContract(self.contract_name, df=self.one_column_dataframe)
        contract.options.distribution['cols_to_ignore'] = []
        contract.options.distribution['cols_to_include'] = []

        with self.assertRaises(ValueError) as ex:
            contract.validate(self.one_column_dataframe)

        self.assertIn('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes', ex.exception.args)

    def _test_data_contract_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name)
        self.assertEqual(default_value, getattr(contract.options, option_name))

    def _test_distribution_check_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name)
        self.assertEqual(default_value, contract.options.distribution[option_name])