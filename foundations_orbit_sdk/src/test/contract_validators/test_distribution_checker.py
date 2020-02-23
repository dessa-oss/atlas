
import numpy
import pandas
from foundations_spec import *

from foundations_orbit.contract_validators.distribution_checker import DistributionChecker

class TestDistributionChecker(Spec):

    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()

    @let_now
    def one_column_dataframe(self):
        return pandas.DataFrame(columns=[self.column_name], data=[4], dtype=numpy.int8)

    @let_now
    def one_column_dataframe_reference_types(self):
        return {self.column_name: 'int'}
    
    @let_now
    def two_column_dataframe(self):
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[5,6],[10,32]], dtype=numpy.int8)
    
    @let_now
    def two_column_dataframe_no_special_values_no_zeros(self):
        return pandas.DataFrame({
            self.column_name: [1,2,4,10,12],
            self.column_name_2: [10, 20, 32, 50, 100]
        })
    
    @let_now
    def two_column_dataframe_reference_types(self):
        return {self.column_name: 'int8', self.column_name_2: 'int8'}

    @let
    def bin_stats_two_column_no_special_value(self):
        return {
            self.column_name: [{
                'percentage': 1.0,
                'upper_edge': 10
            },  {'percentage': 0.0, 'upper_edge': numpy.inf}],
            self.column_name_2: [{
                'percentage': 1.0,
                'upper_edge': 32
            },  {'percentage': 0.0, 'upper_edge': numpy.inf}]
        }

    @let
    def bin_stats_two_column_no_special_value_no_zeros(self):
        return {
            self.column_name: [{
                'percentage': 0.6,
                'upper_edge': 4
            }, {'percentage': 0.4, 'upper_edge': numpy.inf}]
        }

    @let
    def column_name(self):
        return self.faker.word()

    @let
    def column_name_2(self):
        return self._generate_distinct([self.column_name], self.faker.word)

    @let
    def categorical_attributes_one_numerical_column(self):
        return {self.column_name:False}
    
    @let
    def categorical_attributes_two_numerical_columns(self):
        return {self.column_name:False, self.column_name_2:False}
        
    @let_now
    def two_column_dataframe_no_rows(self):
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2])

    def _generate_distinct(self, reference_values, generating_callback):
        candidate_value = generating_callback()
        return candidate_value if candidate_value not in reference_values else self._generate_distinct(reference_values, generating_callback)

    def test_string_cast_for_distribution_checker_returns_expected_information(self):
        self.maxDiff = None
        checker = DistributionChecker([self.column_name], reference_column_types={self.column_name: 'int'}, categorical_attributes=self.categorical_attributes_one_numerical_column)
        checker._distribution_options['max_bins'] = 2
        checker.create_and_set_bin_stats(self.two_column_dataframe_no_special_values_no_zeros)

        expected_information = {
            'distribution_options': checker._distribution_options,
            'bin_stats': self.bin_stats_two_column_no_special_value_no_zeros,
            'reference_column_names': {self.column_name},
            'reference_column_types': {
                self.column_name: 'int'
            }
        }

        self.assertEqual(str(expected_information), str(checker))

    def test_info_dict_for_distribution_checker_returns_expected_information(self):
        self.maxDiff = None
        checker = DistributionChecker([self.column_name], reference_column_types={self.column_name: 'int'}, categorical_attributes=self.categorical_attributes_one_numerical_column)
        checker._distribution_options['max_bins'] = 2
        checker.create_and_set_bin_stats(self.two_column_dataframe_no_special_values_no_zeros)

        expected_information = {
            'distribution_options': checker._distribution_options,
            'bin_stats': self.bin_stats_two_column_no_special_value_no_zeros,
            'reference_column_names': {self.column_name},
            'reference_column_types': {
                self.column_name: 'int'
            }
        }

        self.assertEqual(expected_information, checker.info())

    def test_distribution_check_throws_error_if_dataframe_is_none_when_validate_called(self):
        with self.assertRaises(ValueError) as ex:
            DistributionChecker([], {}, categorical_attributes={}).validate(None)

    def test_distribution_check_throws_error_if_dataframe_is_empty_when_validate_called(self):
        with self.assertRaises(ValueError) as ex:
            checker = DistributionChecker([], {}, {})
            checker.validate(self.empty_dataframe)

    def test_distribution_check_single_column_dataframe_against_itself_returns_dist_check_result_with_one_entry(self):
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.0,
                'binned_passed': True
            }
        }
        distribution_checker = DistributionChecker([self.column_name], self.one_column_dataframe_reference_types,categorical_attributes=self.categorical_attributes_one_numerical_column)
        distribution_checker.create_and_set_bin_stats(self.one_column_dataframe)
        self.assertEqual(expected_dist_check_result, distribution_checker.validate(self.one_column_dataframe))

    def test_distribution_check_multiple_column_dataframe_against_itself_returns_dist_check_result_with_multiple_entries(self):
        
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.0, 
                'binned_passed': True
            }, 
            self.column_name_2: {
                'binned_l_infinity': 0.0, 
                'binned_passed': True
            }}

        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.create_and_set_bin_stats(self.two_column_dataframe)
        validate_results = checker.validate(self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)

    def test_distribution_check_single_column_dataframe_for_non_special_values_in_bin(self):
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
            }
        }

        reference_dataframe = pandas.DataFrame({self.column_name: [1]})

        checker = DistributionChecker([self.column_name], self.one_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_one_numerical_column)
        checker.create_and_set_bin_stats(reference_dataframe)
        self.assertEqual(expected_dist_check_result, checker.validate(self.one_column_dataframe))

    def test_distribution_check_one_column_dataframe_with_upper_edge(self):
        bin_stats = {
             self.column_name: [{
                'value': 1,
                'percentage': 1.0,
                'upper_edge': 20
            }]
        }

        reference_dataframe = pandas.DataFrame({self.column_name: [20]})
        
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 1.0,
                'binned_passed': False,
            }
        }

        checker = DistributionChecker([self.column_name], self.one_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_one_numerical_column)
        checker.create_and_set_bin_stats(reference_dataframe)
        self.assertEqual(expected_dist_check_result, checker.validate(self.one_column_dataframe))

    def test_distribution_check_with_large_value_ranges(self):
        data = {
            self.column_name: [100,25,46],
            self.column_name_2: [50, 2, 400]
        }
        dataframe = pandas.DataFrame(data)
        
        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.5,
                'binned_passed': False,
            },
            self.column_name_2: {
                'binned_l_infinity':  0.167,
                'binned_passed': False,
            }
        }

        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.create_and_set_bin_stats(self.two_column_dataframe)
        validate_results = checker.validate(dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)

    def test_multiple_column_dataframe_will_only_produce_results_for_columns_specified_in_configure(self):
        
        expected_dist_check_result = {
            self.column_name_2: {
                'binned_l_infinity': 0.0, 
                'binned_passed': True
            }}

        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.exclude(attributes = [self.column_name])
        checker.create_and_set_bin_stats(self.two_column_dataframe)
        validate_results = checker.validate(self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_run_with_all_columns_excluded_returns_empty_dictionary(self):

        expected_dist_check_result = {}
    
        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.exclude(attributes='all')
        validate_results = checker.validate(self.two_column_dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_uses_defaults_when_run(self):

        data = {
            self.column_name: [1,2,3,4,5,6,7,8,9,1.5,100],
            self.column_name_2: [50,2,400,51,52,53,54,55,56,57,58]
        }
        dataframe = pandas.DataFrame(data)
        

        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.227,
                'binned_passed': 0.227 < checker._distribution_options['default_threshold'],
            },
            self.column_name_2: {
                'binned_l_infinity':  0.409,
                'binned_passed': 0.409 < checker._distribution_options['default_threshold'],
            }
        }

        checker.create_and_set_bin_stats(self.two_column_dataframe)

        validate_results = checker.validate(dataframe)
        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_runs_test_on_all_column_names_that_are_configured(self):

        data = {
            self.column_name: [1,2,3],
            self.column_name_2: [4,5,6]
        }
        dataframe = pandas.DataFrame(data)
        
        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name])
        checker.configure(attributes=[self.column_name_2])
        checker.create_and_set_bin_stats(self.two_column_dataframe)

        validate_results = checker.validate(dataframe)

        self.assertIn(self.column_name, validate_results)
        self.assertIn(self.column_name_2, validate_results)

    def test_distribution_checker_runs_test_on_all_column_names_that_are_configured_with_threshold(self):

        data = {
            self.column_name: [1,2,12],
            self.column_name_2: [50, 2, 400]
        }
        dataframe = pandas.DataFrame(data)

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity': 0.167,
                'binned_passed': False,
            },
            self.column_name_2: {
                'binned_l_infinity':  0.167,
                'binned_passed': True,
            }
        }
        
        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.exclude(attributes='all')
        checker.configure(attributes=[self.column_name])
        checker.configure(attributes=[self.column_name_2], threshold=0.7)
        checker.create_and_set_bin_stats(self.two_column_dataframe)

        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_runs_test_as_expected_on_columns_configured_with_psi_method(self):
        data = {
            self.column_name: [1,2,12],
            self.column_name_2: [50, 2, 400]
        }
        dataframe = pandas.DataFrame(data)

        expected_dist_check_result = {
            self.column_name: {
                'binned_psi':  0.019,
                'binned_passed': True,
            },
            self.column_name_2: {
                'binned_psi': 0.293,
                'binned_passed': False,
        
            }
        }
        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.configure(attributes=[self.column_name, self.column_name_2], method='psi')
        checker._distribution_options['max_bins'] = 2
        checker.create_and_set_bin_stats(self.two_column_dataframe_no_special_values_no_zeros)

        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)

    def test_distribution_checker_runs_test_as_expected_on_columns_configured_with_different_methods(self):
        data = {
            self.column_name: [1,2,12],
            self.column_name_2: [50, 2, 400]
        }
        dataframe = pandas.DataFrame(data)

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity':  0.067,
                'binned_passed': True,
            },
            self.column_name_2: {
                'binned_psi': 0.293,
                'binned_passed': False,
            }
        }

        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.configure(attributes=[self.column_name], method='l_infinity')
        checker.configure(attributes=[self.column_name_2], method='psi')
        checker._distribution_options['max_bins'] = 2

        checker.create_and_set_bin_stats(self.two_column_dataframe_no_special_values_no_zeros)

        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)

    def test_distribution_checker_configure_raises_value_error_when_unsupported_columns_used(self):
        reference_column_types = {self.column_name: 'int', self.column_name_2: 'object'}
        checker = DistributionChecker([self.column_name, self.column_name_2], reference_column_types=reference_column_types, categorical_attributes=self.categorical_attributes_two_numerical_columns)
        checker.configure(attributes=[self.column_name], threshold=0.1, method='l_infinity')

        expected_error_dictionary = {
            self.column_name_2: 'Invalid Type: object'
        }

        with self.assertRaises(ValueError) as e:
            checker.configure(attributes=[self.column_name_2], threshold=0.1, method='l_infinity')

        self.assertEqual(f'The following columns have errors: {expected_error_dictionary}', e.exception.args[0])
    
    def test_distribution_checker_provides_expected_output_when_given_categorical_data(self):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats, create_bin_stats_categorical

        data = {
            self.column_name: [1,1,1,2,2,2],
            self.column_name_2: [1.0]*6
        }
        dataframe = pandas.DataFrame(data)
        categorical_attributes = {self.column_name:True, self.column_name_2:False}

        bin_stats = {}
        bin_stats[self.column_name] = create_bin_stats_categorical(col_values=dataframe[self.column_name])
        bin_stats[self.column_name_2] = create_bin_stats(max_bins=10, col_values=dataframe[self.column_name_2])

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity':  0.0,
                'binned_passed': True,
            },
            self.column_name_2: {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
            }
        }

        checker = DistributionChecker([self.column_name, self.column_name_2], self.two_column_dataframe_reference_types, categorical_attributes=categorical_attributes)
        checker.configure(attributes=[self.column_name], method='l_infinity')
        checker.configure(attributes=[self.column_name_2], method='l_infinity')
        checker.create_and_set_bin_stats(dataframe)
        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)
    
    def test_distribution_checker_provides_expected_output_when_given_categorical_data_and_using_l_infinity(self):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats, create_bin_stats_categorical
        import numpy

        data = {
            self.column_name: [1,1,1,2,2,2],
        }

        dataframe = pandas.DataFrame(data)
        categorical_attributes = {self.column_name:True}

        bin_stats = {}
        bin_stats[self.column_name] = create_bin_stats_categorical(col_values=dataframe[self.column_name])

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity':  0.333,
                'binned_passed': False,
            },
        }
        checker = DistributionChecker([self.column_name], self.one_column_dataframe_reference_types, categorical_attributes=categorical_attributes)
        checker.configure(attributes=[self.column_name], method='l_infinity')
        
        checker.create_and_set_bin_stats(dataframe)

        dataframe.iloc[0,0] = self.faker.pyint()
        dataframe.iloc[1,0] = self.faker.pyint()

        validate_results = checker.validate(dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)

    def test_distribution_checker_provides_expected_output_with_zeros_input(self):
        from foundations_orbit.contract_validators.utils.create_bin_stats import create_bin_stats, create_bin_stats_categorical
        import numpy

        reference_data = {
            self.column_name: [0]*99 + [1],
        }

        reference_dataframe = pandas.DataFrame(reference_data)

        categorical_attributes = {self.column_name:True}

        bin_stats = {}
        bin_stats[self.column_name] = create_bin_stats_categorical(col_values=reference_dataframe[self.column_name])

        expected_dist_check_result = {
            self.column_name: {
                'binned_l_infinity':  0.0,
                'binned_passed': True,
            },
        }
        checker = DistributionChecker([self.column_name], self.one_column_dataframe_reference_types, categorical_attributes=categorical_attributes)
        checker.configure(attributes=[self.column_name], method='l_infinity')
        checker.create_and_set_bin_stats(reference_dataframe)

        validate_results = checker.validate(reference_dataframe)

        self.assertEqual(expected_dist_check_result, validate_results)

    def test_configure_with_nonexistent_attributes_throws_correct_error(self):
        reference_data = {
            self.column_name: [0]*99 + [1],
        }

        reference_dataframe = pandas.DataFrame(reference_data)
        categorical_attributes = {self.column_name:True}

        checker = DistributionChecker([self.column_name], self.one_column_dataframe_reference_types, categorical_attributes=categorical_attributes)
        
        with self.assertRaises(ValueError) as ex:
            checker.configure(attributes=[self.column_name_2], method='l_infinity')

        expected_error_message = {
            self.column_name_2: 'Invalid Column Name: Does not exist in reference'
        }

        self.assertEqual(f'The following columns have errors: {expected_error_message}', str(ex.exception))

