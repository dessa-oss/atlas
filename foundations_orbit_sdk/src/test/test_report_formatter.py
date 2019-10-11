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
    def monitor_package(self):
        return self.faker.sentence()

    @let
    def contract_name(self):
        return self.faker.sentence()

    @let
    def column_list(self):
        return [self.column_name, self.column_name_2, self.column_name_3]

    @let
    def type_mapping(self):
        mapping = {column: self.faker.word() for column in self.column_list}
        mapping[self.column_name_4] = self.faker.word()

        return mapping

    @let
    def number_of_columns(self):
        return 3

    @let
    def distribution_checks(self):
        return {column: self.gen_dist_chect_result() for column in self.column_list}

    @set_up
    def set_up(self):
        self.data_contract_options = Mock()
        self.data_contract_options.check_distribution = True

    @let
    def validation_report(self):
        return {
            'schema_check_results': {
                'passed': False,
                'error_message': ''
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
            },
            'dist_check_results': self.distribution_checks
        }

    @let
    def column_name(self):
        return self.faker.sentence()

    @let
    def column_name_2(self):
        return self.faker.sentence()

    @let
    def column_name_3(self):
        return self.faker.sentence()

    @let
    def column_name_4(self):
        return self.faker.sentence()

    @let
    def row_count_diff(self):
        return self.faker.random.random()

    def gen_dist_chect_result(self):
        return {
            'binned_passed': True,
            'binned_l_infinity': 0.2,
            'special_values':{
                'nan':{
                    'percentage_diff': 0.15,
                    'ref_percentage': 0,
                    'current_percentage': 0.15,
                    'passed': True
                }
            }
        }

    def test_report_formatter_returns_formatted_report_with_expected_date(self):
        self.validation_report['schema_check_results'] = {'passed': True}
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.inference_period, formatted_report['date'])

    def test_report_formatter_returns_formatted_report_with_expected_monitor_package(self):
        self.validation_report['schema_check_results'] = {'passed': True}
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.monitor_package, formatted_report['monitor_package'])

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
            'healthy': self.number_of_columns,
            'critical': 0,
            'warning': 0
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_report, formatted_report['schema']['summary'])

    def test_report_formatter_return_details_by_attribute_when_all_schema_check_passed(self):
        self.validation_report['schema_check_results'] = {'passed': True}
        expected_detail_for_attribute = []
        
        for column in self.column_list:
            expected_detail_for_attribute.append({
                'attribute_name': column,
                'data_type': self.type_mapping[column],
                'issue_type': None,
                'validation_outcome': 'healthy'
            })

        self._sort_check_for_details_by_activity(expected_detail_for_attribute)


    def test_report_formatter_returns_critical_schema_summary_if_schema_check_failed_when_current_has_one_more_column(self):
        columns_in_current_dataframe = list(self.column_list)
        columns_in_current_dataframe.append(self.column_name_4)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [self.column_name_4],
            'missing_in_current': []
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns,
            'critical': 1,
            'warning': 0
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
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns - 1,
            'critical': 1,
            'warning': 0
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
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns - 1,
            'critical': 1,
            'warning': 0
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['schema']['summary'])

    def test_report_formatter_returns_critical_schema_summary_if_schema_check_failed_when_reference_has_one_unshared_column_and_current_has_two_unshared_columns(self):
        columns_in_current_dataframe = list(self.column_list)
        column_missing_from_current = columns_in_current_dataframe.pop()

        column_missing_from_reference = self.column_name_4
        columns_in_current_dataframe.append(column_missing_from_reference)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [column_missing_from_reference],
            'missing_in_current': [column_missing_from_current]
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns - 1,
            'critical': 1,
            'warning': 0
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['schema']['summary'])

    def test_report_formatter_return_throws_exception_when_schema_check_failed_and_no_error_msg(self):
        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': '',
            'missing_in_ref': [],
            'missing_in_current': []
        }

        with self.assertRaises(ValueError) as error:
            self._generate_formatted_report()
        self.assertIn('Invalid error message', error.exception.args)

    def test_report_formatter_returns_critical_schema_summary_if_schema_check_failed_when_reference_has_two_unshared_columns_and_current_has_one_unshared_column(self):
        columns_in_current_dataframe = self.column_list
        columns_in_reference_dataframe = list(self.column_list)

        column_missing_from_reference = columns_in_reference_dataframe.pop()
        
        column_missing_from_current = self.column_name_4
        columns_in_reference_dataframe.append(column_missing_from_current)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [column_missing_from_reference],
            'missing_in_current': [column_missing_from_current]
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
            'critical': 1,
            'warning': 0
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
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }

        expected_details_for_attribute = []
        for column in self.column_list:
            expected_details_for_attribute.append({
                'attribute_name': column,
                'data_type': self.type_mapping[column],
                'issue_type': 'missing in current dataframe' if column == missing_in_current else None,
                'validation_outcome': 'critical' if column == missing_in_current else 'healthy'
            })
        
        self._sort_check_for_details_by_activity(expected_details_for_attribute)

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

        all_columns = self.column_list
        expected_detail_for_attribute = []

        for column in all_columns:
            detail = {
                'attribute_name': column,
                'data_type': self.type_mapping[column],
                'issue_type': None,
                'validation_outcome': 'healthy'
            }
            if column == self.column_name or column == self.column_name_2:
                detail['issue_type'] = 'missing in current dataframe'
                detail['validation_outcome'] = 'critical'

            expected_detail_for_attribute.append(detail)
        
        self._sort_check_for_details_by_activity(expected_detail_for_attribute)
        
    def test_report_formatter_returns_details_by_attribute_if_schema_check_failed_when_reference_has_two_difference_column(self):
        columns_in_reference_dataframe = self.column_list
        columns_in_current_dataframe = list(self.column_list)

        columns_missing_from_reference = [self.column_name, self.column_name_2]

        for column_missing_from_reference in columns_missing_from_reference:
            index_at_which_to_insert = self.faker.random.randint(0, len(columns_in_current_dataframe))
            columns_in_current_dataframe.insert(index_at_which_to_insert, column_missing_from_reference)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': columns_missing_from_reference,
            'missing_in_current': []
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }
        self.validation_report['metadata']['reference_metadata'] = {
            'column_names': columns_in_reference_dataframe,
            'type_mapping': self.type_mapping
        }

        all_columns = self._get_all_columns_list(columns_in_current_dataframe, columns_in_reference_dataframe)

        expected_detail_for_attribute = []
        for column in all_columns:
            detail = {
                'attribute_name': column,
                'data_type': self.type_mapping[column],
                'issue_type': None,
                'validation_outcome': 'healthy'
            }
            if column == self.column_name or column == self.column_name_2:
                detail['issue_type'] = 'missing in reference dataframe'
                detail['validation_outcome'] = 'critical'

            expected_detail_for_attribute.append(detail)

        self._sort_check_for_details_by_activity(expected_detail_for_attribute)

    def test_report_formatter_returns_details_by_attribute_if_schema_check_failed_when_current_and_reference_each_have_one_column_the_other_does_not(self):
        columns_in_current_dataframe = list(self.column_list)
        column_missing_from_current = columns_in_current_dataframe.pop()

        index_at_which_to_insert = self.faker.random.randint(0, len(columns_in_current_dataframe))

        column_missing_from_reference = self.column_name_4
        columns_in_current_dataframe.insert(index_at_which_to_insert, column_missing_from_reference)

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column sets not equal',
            'missing_in_ref': [column_missing_from_reference],
            'missing_in_current': [column_missing_from_current]
        }

        self.validation_report['metadata']['current_metadata'] = {
            'column_names': columns_in_current_dataframe,
            'type_mapping': self.type_mapping
        }

        all_columns = self._get_all_columns_list(columns_in_current_dataframe, list(self.column_list))
        
        expected_detail_for_attribute = []
        for column in all_columns:
            detail = {
                'attribute_name': column,
                'data_type': self.type_mapping[column],
                'issue_type': None,
                'validation_outcome': 'healthy'
            }
            if column == column_missing_from_current:
                detail['issue_type'] = 'missing in current dataframe'
                detail['validation_outcome'] = 'critical'
            if column == column_missing_from_reference:
                detail['issue_type'] = 'missing in reference dataframe'
                detail['validation_outcome'] = 'critical'

            expected_detail_for_attribute.append(detail)

        self._sort_check_for_details_by_activity(expected_detail_for_attribute)

    def test_report_formatter_returns_details_by_attribute_for_one_column_not_in_order(self):
        
        column_out_of_order = list(self.column_list)[0]

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'columns not in order',
            'columns_out_of_order': [column_out_of_order],
        }

        expected_detail_for_attribute = [{
            'attribute_name': column_out_of_order,
            'data_type': self.type_mapping[column_out_of_order],
            'issue_type': 'column is out of order',
            'validation_outcome': 'critical'
        }]

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_detail_for_attribute, formatted_report['schema']['details_by_attribute'])

    def test_report_formatter_returns_details_by_attribute_for_two_columns_not_in_order(self):
        
        column_out_of_order = list(self.column_list)[0]
        column_2_out_of_order = list(self.column_list)[1]

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'columns not in order',
            'columns_out_of_order': [column_out_of_order,  column_2_out_of_order],
        }

        expected_detail_for_attribute = [{
            'attribute_name': column_out_of_order,
            'data_type': self.type_mapping[column_out_of_order],
            'issue_type': 'column is out of order',
            'validation_outcome': 'critical'
        },{
            'attribute_name': column_2_out_of_order,
            'data_type': self.type_mapping[column_2_out_of_order],
            'issue_type': 'column is out of order',
            'validation_outcome': 'critical'
        }]

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_detail_for_attribute, formatted_report['schema']['details_by_attribute'])

    def test_report_formatter_return_summary_for_two_columns_not_in_order(self):
        column_out_of_order = list(self.column_list)[0]
        column_2_out_of_order = list(self.column_list)[1]

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'columns not in order',
            'columns_out_of_order': [column_out_of_order,  column_2_out_of_order],
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns - 2,
            'critical': 2,
            'warning': 0
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['schema']['summary'])

    def test_report_formatter_returns_details_by_attribute_for_column_datatype_mismatches_when_one_current_column_is_mismatched(self):
        
        column_mismatched = list(self.column_list)[0]

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column datatype mismatches',
            'cols': [column_mismatched],
        }

        self.validation_report['metadata']['current_metadata']['type_mapping'][column_mismatched] = 'unknown'

        expected_detail_for_attribute = [{
            'attribute_name': column_mismatched,
            'data_type': 'unknown',
            'issue_type': f'datatype in reference dataframe is {self.type_mapping[column_mismatched]}',
            'validation_outcome': 'critical'
        }]

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_detail_for_attribute, formatted_report['schema']['details_by_attribute'])

    def test_report_formatter_returns_details_by_attribute_for_column_datatype_mismatches_when_two_current_column_is_mismatched(self):
        
        column_mismatched = list(self.column_list)[0]
        column_2_mismatched = list(self.column_list)[1]

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column datatype mismatches',
            'cols': [column_mismatched, column_2_mismatched],
        }

        self.validation_report['metadata']['current_metadata']['type_mapping'][column_mismatched] = 'unknown'
        self.validation_report['metadata']['current_metadata']['type_mapping'][column_2_mismatched] = 'unknown'

        expected_detail_for_attribute = [{
            'attribute_name': column_mismatched,
            'data_type': 'unknown',
            'issue_type': f'datatype in reference dataframe is {self.type_mapping[column_mismatched]}',
            'validation_outcome': 'critical'
        }, {
            'attribute_name': column_2_mismatched,
            'data_type': 'unknown',
            'issue_type': f'datatype in reference dataframe is {self.type_mapping[column_2_mismatched]}',
            'validation_outcome': 'critical'
        }]

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_detail_for_attribute, formatted_report['schema']['details_by_attribute'])

    def test_report_formatter_return_summary_for_column_datatype_mismatches_when_two_current_column_is_mismatched(self):
        column_mismatched = list(self.column_list)[0]
        column_2_mismatched = list(self.column_list)[1]

        self.validation_report['schema_check_results'] = {
            'passed': False,
            'error_message': 'column datatype mismatches',
            'cols': [column_mismatched,  column_2_mismatched],
        }

        expected_schema_summary = {
            'healthy': self.number_of_columns - 2,
            'critical': 2,
            'warning': 0
        }

        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['schema']['summary'])

    def test_return_data_quality_summary_when_all_is_healthy(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        expected_schema_summary = {
            'healthy': self.number_of_columns,
            'critical': 0,
            'warning': 0
        }
        
        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['data_quality']['summary'])

    def test_return_data_quality_attribute_details_when_all_is_healthy(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        data_quality_attribute_details = []
        
        for column, details in self.distribution_checks.items():
            for sv in details['special_values']:
                attribute_details = {
                    'attribute_name': column,
                    'value': f'{sv}',
                    'pct_in_reference_data': 0,
                    'pct_in_current_data': 0.15,
                    'difference_in_pct': 0.15,
                    'validation_outcome': 'healthy',
                }
                data_quality_attribute_details.append(attribute_details)

        formatted_report = self._generate_formatted_report()
        self.assertEqual(data_quality_attribute_details, formatted_report['data_quality']['details_by_attribute'])

    def test_return_data_quality_summary_when_one_column_is_unhealthy(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        unhealthy_column = list(self.column_list)[0]
        self.validation_report['dist_check_results'][unhealthy_column]['special_values']['nan']['passed'] = False

        expected_schema_summary = {
            'healthy': self.number_of_columns - 1,
            'critical': 1,
            'warning': 0
        }
        
        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['data_quality']['summary'])

    def test_return_data_quality_details_when_one_column_is_unhealthy(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        data_quality_attribute_details = []
        
        unhealthy_column = list(self.column_list)[0]
        self.validation_report['dist_check_results'][unhealthy_column]['special_values']['nan']['passed'] = False

        for column, details in self.distribution_checks.items():
            for sv in details['special_values']:
                attribute_details = {
                    'attribute_name': column,
                    'value': f'{sv}',
                    'pct_in_reference_data': 0,
                    'pct_in_current_data': 0.15,
                    'difference_in_pct': 0.15,
                    'validation_outcome': 'critical' if column == unhealthy_column else 'healthy',
                }
                data_quality_attribute_details.append(attribute_details)

        formatted_report = self._generate_formatted_report()
        self.assertEqual(data_quality_attribute_details, formatted_report['data_quality']['details_by_attribute'])

    def test_return_population_shift_summary_when_all_columns_are_healthy(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        expected_schema_summary = {
            'healthy': self.number_of_columns,
            'critical': 0,
            'warning': 0
        }
        
        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['population_shift']['summary'])

    def test_return_population_shift_details_when_all_columns_are_healthy(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        population_shift_attribute_details = []

        for column, details in self.distribution_checks.items():
            population_shift_attribute_details.append({
                'attribute_name': column,
                'L-infinity': 0.2,
                'validation_outcome': 'healthy',
            })
        
        formatted_report = self._generate_formatted_report()
        self.assertEqual(population_shift_attribute_details, formatted_report['population_shift']['details_by_attribute'])
    
    def test_return_population_shift_summary_when_one_columns_is_unhealthy(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        unhealthy_column = list(self.column_list)[0]
        self.validation_report['dist_check_results'][unhealthy_column]['binned_passed'] = False

        expected_schema_summary = {
            'healthy': self.number_of_columns - 1,
            'critical': 1,
            'warning': 0
        }
        
        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_schema_summary, formatted_report['population_shift']['summary'])
    
    def test_return_population_shift_details_when_one_columns_is_unhealthy(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        unhealthy_column = list(self.column_list)[0]
        self.validation_report['dist_check_results'][unhealthy_column]['binned_passed'] = False

        population_shift_attribute_details = []
        
        for column, details in self.distribution_checks.items():
            population_shift_attribute_details.append({
                'attribute_name': column,
                'L-infinity': 0.2,
                'validation_outcome': 'critical' if column == unhealthy_column else 'healthy',
            })
        
        formatted_report = self._generate_formatted_report()
        self.assertEqual(population_shift_attribute_details, formatted_report['population_shift']['details_by_attribute'])
    
    def test_return_no_data_quality_if_check_distribution_is_false(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        self.data_contract_options.check_distribution = False
        formatted_report = self._generate_formatted_report()
        self.assertEqual({}, formatted_report['data_quality'])

    def test_return_no_population_shift_if_check_distribution_is_false(self):
        self.validation_report['schema_check_results'] = {'passed': True}

        self.data_contract_options.check_distribution = False
        formatted_report = self._generate_formatted_report()
        self.assertEqual({}, formatted_report['population_shift'])

    def _sort_check_for_details_by_activity(self, expected_detail_for_attribute):
        expected_detail_for_attribute.sort(key=lambda detail: (detail['validation_outcome'], detail['attribute_name']))
        formatted_report = self._generate_formatted_report()
        self.assertEqual(expected_detail_for_attribute, formatted_report['schema']['details_by_attribute'])

    
    def _get_all_columns_list(self, columns_in_current_dataframe, columns_in_reference_dataframe):
        in_current_not_in_reference = set(columns_in_current_dataframe) - set(columns_in_reference_dataframe)
        return columns_in_reference_dataframe + list(in_current_not_in_reference)

    def _generate_formatted_report(self):
        formatter = ReportFormatter(inference_period=self.inference_period,
                                    monitor_package=self.monitor_package,
                                    contract_name=self.contract_name,
                                    validation_report=self.validation_report,
                                    options=self.data_contract_options)

        return formatter.formatted_report()