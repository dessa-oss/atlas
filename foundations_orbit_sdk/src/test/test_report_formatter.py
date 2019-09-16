"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_orbit.report_formatter import ReportFormatter


class TestReportFormatter(Spec):

    @let
    def inference_period(self):
        return self.faker.date()
    @let
    def model_package(self):
        return self.faker.word()

    @let
    def contract_name(self):
        return self.faker.word()

    @let
    def column_list(self):
        return [self.faker.word() for _ in range(self.number_of_columns)]

    @let
    def type_mapping(self):
        mapping = {column: self.faker.word() for column in self.column_list}
        mapping[self.column_name] = self.faker.word()
        mapping[self.column_name_2] = self.faker.word()

        return mapping

    @let
    def number_of_columns(self):
        return self.faker.random.randint(1, 5)

    @let
    def validation_report(self):
        return {
            'schema_check_results': {
                'passed': False
            },
            'metadata': {
                'reference_metadata': {
                    'column_names': self.column_list,
                    'type_mapping': self.type_mapping
                },
                'current_metadata': {
                    'column_names': self.column_list,
                    'type_mapping': self.type_mapping
                }
            }
        }

    @let
    def column_name(self):
        return self.faker.word()

    @let
    def column_name_2(self):
        return self.faker.word()

    @let
    def row_count_diff(self):
        return self.faker.random.random()

    def test_report_formatter_returns_formatted_report_with_expected_date(self):
        self.validation_report['schema_check_results'] = {'passed': True}
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.inference_period, formatted_report['date'])

    def test_report_formatter_returns_formatted_report_with_expected_model_package(self):
        self.validation_report['schema_check_results'] = {'passed': True}
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.model_package, formatted_report['model_package'])

    def test_report_formatter_returns_formatted_report_with_expected_data_contract(self):
        self.validation_report['schema_check_results'] = {'passed': True}
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.contract_name, formatted_report['data_contract'])

    def test_report_formatter_returns_formatted_report_with_expected_row_cnt_diff_if_does_not_exist(self):
        self.validation_report['schema_check_results'] = {'passed': True}
        formatted_report = self._generate_formatted_report()
        self.assertEqual(0, formatted_report['row_cnt_diff'])

    def test_report_formatter_returns_formatted_report_with_expected_row_cnt_diff_if_exist(self):
        self.validation_report['schema_check_results'] = {'passed': True}
        self.validation_report['row_cnt_diff'] = self.row_count_diff
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.row_count_diff, formatted_report['row_cnt_diff'])

    def test_report_formatter_returns_healthy_schema_summary_if_schema_check_passed(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        expected_schema_report = {
            'summary': {
                'healthy': self.number_of_columns,
                'critical': 0
            }
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_report, formatted_report['schema'])

    def test_report_formatter_returns_critical_schema_summary_if_schema_check_failed_when_current_has_one_more_column(self):
        columns_in_current_dataframe = list(self.column_list)
        columns_in_current_dataframe.append(self.column_name)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [self.column_name],
            'missing_in_current': []
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns,
            'critical': 1
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['schema']['summary'])

    def test_report_formatter_returns_critical_schema_summary_if_schema_check_failed_when_current_has_one_less_column(self):
        columns_in_current_dataframe = list(self.column_list)
        missing_in_current = columns_in_current_dataframe.pop()

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [],
            'missing_in_current': [missing_in_current]
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns - 1,
            'critical': 1
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['schema']['summary'])

    def test_report_formatter_returns_critical_schema_summary_if_schema_check_failed_when_current_and_reference_each_have_one_column_the_other_does_not(self):
        columns_in_current_dataframe = list(self.column_list)
        column_missing_from_current = columns_in_current_dataframe.pop()

        index_at_which_to_insert = self.faker.random.randint(0, len(columns_in_current_dataframe))

        column_missing_from_reference = self.column_name
        columns_in_current_dataframe.insert(index_at_which_to_insert, column_missing_from_reference)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [column_missing_from_reference],
            'missing_in_current': [column_missing_from_current]
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns - 1,
            'critical': 1
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['schema']['summary'])

    def test_report_formatter_returns_critical_schema_summary_if_schema_check_failed_when_reference_has_one_unshared_column_and_current_has_two_unshared_columns(self):
        columns_in_current_dataframe = list(self.column_list)
        column_missing_from_current = columns_in_current_dataframe.pop()

        columns_missing_from_reference = [self.column_name, self.column_name_2]

        for column_missing_from_reference in columns_missing_from_reference:
            index_at_which_to_insert = self.faker.random.randint(0, len(columns_in_current_dataframe))
            columns_in_current_dataframe.insert(index_at_which_to_insert, column_missing_from_reference)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': columns_missing_from_reference,
            'missing_in_current': [column_missing_from_current]
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns - 1,
            'critical': 2
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['schema']['summary'])

    def test_report_formatter_returns_critical_schema_summary_if_schema_check_failed_when_reference_has_two_unshared_columns_and_current_has_one_unshared_column(self):
        columns_in_current_dataframe = self.column_list
        columns_in_reference_dataframe = list(self.column_list)
        column_missing_from_reference = columns_in_reference_dataframe.pop()

        columns_missing_from_current = [self.column_name, self.column_name_2]

        for column_missing_from_current in columns_missing_from_current:
            index_at_which_to_insert = self.faker.random.randint(0, len(columns_in_reference_dataframe))
            columns_in_reference_dataframe.insert(index_at_which_to_insert, column_missing_from_current)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [column_missing_from_reference],
            'missing_in_current': columns_missing_from_current
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }

        self.validation_report['metadata']['reference_metadata'] = {
            'column_names': columns_in_reference_dataframe,
            'type_mapping': self.type_mapping
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns - 1,
            'critical': 2
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['schema']['summary'])

    def test_report_formatter_returns_details_by_attribute_if_schema_check_failed_when_current_has_one_less_column(self):
        columns_in_current_dataframe = list(self.column_list)
        missing_in_current = columns_in_current_dataframe.pop()

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [],
            'missing_in_current': [missing_in_current]
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe
        }

        expected_detail_for_attribute = {
            'attribute_name': missing_in_current,
            'data_type': self.type_mapping[missing_in_current],
            'issue_type': 'missing in current',
            'validation_outcome': 'error_state'
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_detail_for_attribute, formatted_report['schema']['details_by_attribute'][0])

    def test_report_formatter_returns_details_by_attribute_if_schema_check_failed_when_current_two_difference_column(self):
        columns_in_current_dataframe = self.column_list
        columns_in_reference_dataframe = list(self.column_list)

        columns_missing_from_current = [self.column_name, self.column_name_2]

        for column_missing_from_current in columns_missing_from_current:
            index_at_which_to_insert = self.faker.random.randint(0, len(columns_in_reference_dataframe))
            columns_in_reference_dataframe.insert(index_at_which_to_insert, column_missing_from_current)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [],
            'missing_in_current': columns_missing_from_current
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }
        self.validation_report['metadata']['reference_metadata'] = {
            'column_names': columns_in_reference_dataframe,
            'type_mapping': self.type_mapping
        }

        expected_detail_for_attribute = [{
            'attribute_name': self.column_name,
            'data_type': self.type_mapping[self.column_name],
            'issue_type': 'missing in current',
            'validation_outcome': 'error_state'
        }, {
            'attribute_name': self.column_name_2,
            'data_type': self.type_mapping[self.column_name_2],
            'issue_type': 'missing in current',
            'validation_outcome': 'error_state'
        }]

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_detail_for_attribute, formatted_report['schema']['details_by_attribute'])

    def _generate_formatted_report(self):
        formatter = ReportFormatter(inference_period=self.inference_period,
                                    model_package=self.model_package,
                                    contract_name=self.contract_name,
                                    validation_report=self.validation_report,
                                    options=Mock())

        return formatter.formatted_report()