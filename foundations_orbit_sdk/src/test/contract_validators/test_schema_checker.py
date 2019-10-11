"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.contract_validators.schema_checker import SchemaChecker

class TestSchemaChecker(Spec):
    
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
    def two_column_dataframe_different_types(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2.0]])

    @let_now
    def two_column_dataframe(self):
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

    def test_check_schema_of_empty_dataframe_against_itself_passes(self):
        self._assert_schema_check_results_for_dataframe(self.empty_dataframe, self.empty_dataframe, {'passed': True})

    def test_check_schema_of_dataframe_with_zero_columns_against_dataframe_with_one_column_fails_schema_check(self):
        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [],
            'missing_in_current': [self.column_name]
        }

        self._assert_schema_check_results_for_dataframe(self.one_column_dataframe, self.empty_dataframe, expected_schema_check_results)

    def test_check_schema_of_dataframe_with_one_column_against_another_dataframe_with_one_column_but_different_name_fails_schema_check(self):
        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [self.column_name_2],
            'missing_in_current': [self.column_name]
        }

        self._assert_schema_check_results_for_dataframe(self.one_column_dataframe, self.one_column_dataframe_different_column_name, expected_schema_check_results)

    def test_check_schema_of_dataframe_with_one_column_against_another_dataframe_with_two_columns_first_column_the_same_fails_schema_check(self):
        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [self.column_name_2],
            'missing_in_current': []
        }

        self._assert_schema_check_results_for_dataframe(self.one_column_dataframe, self.two_column_dataframe_no_rows, expected_schema_check_results)

    def test_check_schema_of_dataframe_with_one_column_against_itself_passes_schema_check(self):
        self._assert_schema_check_results_for_dataframe(self.one_column_dataframe, self.one_column_dataframe, {'passed': True})

    def test_check_schema_of_dataframe_with_multiple_columns_against_itself_passes_schema_check(self):
        self._assert_schema_check_results_for_dataframe(self.two_column_dataframe_no_rows, self.two_column_dataframe_no_rows, {'passed': True})

    def test_check_schema_of_dataframe_with_two_columns_against_different_dataframe_with_two_columns_fails_schema_check(self):
        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [self.column_name_3],
            'missing_in_current': [self.column_name_2]
        }

        self._assert_schema_check_results_for_dataframe(self.two_column_dataframe_no_rows, self.two_column_dataframe_no_rows_different_second_column, expected_schema_check_results)

    def test_check_schema_of_column_names_wrong_order_fails_schema_check(self):
        expected_schema_check_results = {
            'passed': False,
            'error_message': 'columns not in order',
            'columns_out_of_order': [self.column_name_2, self.column_name]
        }

        self._assert_schema_check_results_for_dataframe(self.two_column_dataframe_no_rows, self.two_column_dataframe_columns_wrong_order, expected_schema_check_results)

    def test_check_schema_of_column_names_wrong_order_fails_schema_check_more_rows(self):
        expected_schema_check_results = {
            'passed': False,
            'error_message': 'columns not in order',
            'columns_out_of_order': [self.column_name_4, self.column_name]
        }

        self._assert_schema_check_results_for_dataframe(self.four_column_dataframe_no_rows, self.four_column_dataframe_no_rows_different_order, expected_schema_check_results)

    def test_check_schema_of_single_column_dataframe_column_types_fails_when_column_type_does_not_match(self):
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

        self._assert_schema_check_results_for_dataframe(self.one_column_dataframe, self.one_column_dataframe_different_data_type, expected_schema_check_results)

    def test_check_schema_of_two_column_dataframe_column_types_fails_when_column_type_does_not_match(self):
        expected_schema_check_results = {
            'passed': False,
            'error_message': 'column datatype mismatches',
            'cols': {
                self.column_name_2: {
                    'ref_type': 'int64',
                    'current_type': 'float64'
                }
            }
        }

        self._assert_schema_check_results_for_dataframe(self.two_column_dataframe, self.two_column_dataframe_different_types, expected_schema_check_results)

    def test_string_cast_for_schema_check_returns_expected_information(self):
        import json
        import numpy

        schema_checker = self._schema_checker_from_dataframe(self.one_column_dataframe)

        expected_information = {
            'column_names': [self.column_name],
            'column_types': {self.column_name: 'int8'}
        }

        self.assertEqual(json.dumps(expected_information), str(schema_checker))
    
    def test_schema_checker_can_accept_configurations(self):
        schema_checker = self._schema_checker_from_dataframe(self.two_column_dataframe)
        self.assertIsNotNone(getattr(schema_checker, "configure", None))
        
    def test_schema_checker_can_accept_exclusions(self):
        schema_checker = self._schema_checker_from_dataframe(self.two_column_dataframe)
        self.assertIsNotNone(getattr(schema_checker, "exclude", None))

    def test_check_schema_configuration_passes_on_specified_column_with_mismatched_reference_and_current_dataframes(self):
        import pandas, numpy
        reference_dataframe = pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2]])
        current_dataframe = pandas.DataFrame(columns=[self.column_name], data=[[10]])

        schema_checker = self._schema_checker_from_dataframe(reference_dataframe)
        schema_checker.exclude(attributes='all')
        schema_checker.configure(attributes=[self.column_name])
        validation_result = schema_checker.validate(current_dataframe)
        self.assertEqual({'passed': True}, validation_result)

    def test_check_schema_excludes_columns_passes_on_mismatched_reference_and_current_dataframes(self):
        import pandas, numpy
        reference_dataframe = pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2]])
        current_dataframe = pandas.DataFrame(columns=[self.column_name_2], data=[[10]])

        schema_checker = self._schema_checker_from_dataframe(reference_dataframe)
        schema_checker.exclude(attributes=[self.column_name])
        validation_result = schema_checker.validate(current_dataframe)
        self.assertEqual({'passed': True}, validation_result)

    def test_check_schema_with_multiple_calls_to_configuration_appends_to_previous_configurations(self):
        import pandas
        num_rows_columns = 4
        records = []
        
        for row in range(num_rows_columns):
            records.append([])
            for col in range(num_rows_columns):
                records[row].append(col)
        
        reference_dataframe = pandas.DataFrame(columns=[self.column_name, self.column_name_2, self.column_name_3, self.column_name_4], data=records)
        current_dataframe = reference_dataframe.copy()
        schema_checker = self._schema_checker_from_dataframe(reference_dataframe)
        
        schema_checker.exclude(attributes='all')

        schema_checker.configure(attributes=[self.column_name, self.column_name_2])
        schema_checker.configure(attributes=[self.column_name_3, self.column_name_4])

        validation_result = schema_checker.validate(current_dataframe)

        self.assertEqual({'passed': True}, validation_result)

    def test_schema_checker_excludes_all_columns_by_default_and_tests_passed(self):
        import pandas, numpy
        reference_dataframe = pandas.DataFrame(columns=[self.column_name, self.column_name_2], data=[[1, 2]])
        current_dataframe = pandas.DataFrame(columns=[self.column_name_2], data=[[10]])

        schema_checker = self._schema_checker_from_dataframe(reference_dataframe)
        schema_checker.exclude(attributes='all')
        validation_result = schema_checker.validate(current_dataframe)
        self.assertEqual({'passed': True}, validation_result)

    def _dataframe_statistics(self, dataframe):
        column_names = list(dataframe.columns)
        column_types = {column_name: str(dataframe.dtypes[column_name]) for column_name in column_names}

        return column_names, column_types
    
    def _schema_checker_from_dataframe(self, dataframe):
        column_names, column_types = self._dataframe_statistics(dataframe)
        return SchemaChecker(column_names, column_types)

    def _assert_schema_check_results_for_dataframe(self, ref_dataframe, current_dataframe, expected_results):
        schema_checker = self._schema_checker_from_dataframe(ref_dataframe)
        self.assertEqual(expected_results, schema_checker.validate(current_dataframe))