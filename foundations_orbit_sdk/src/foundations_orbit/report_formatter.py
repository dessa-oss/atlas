"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ReportFormatter(object):

    def __init__(self, inference_period, monitor_package, contract_name, job_id, user, validation_report, options):
        self._inference_period = inference_period
        self._monitor_package = monitor_package
        self._contract_name = contract_name
        self._job_id = job_id
        self._user = user
        self._validation_report = validation_report
        self._options = options

    def formatted_report(self):
        formatted_min_max_report = self._formatted_min_max_report()

        return {
            'date': self._inference_period,
            'monitor_package': self._monitor_package,
            'user': self._user,
            'job_id': self._job_id,
            'data_contract': self._contract_name,
            'row_count': self._formatted_row_count_difference_report(),
            'schema': self._formatted_schema_report(),
            'data_quality': self._formatted_data_quality_report() or {},
            'population_shift': self._formatted_population_shift_report() or {},
            'min': formatted_min_max_report['min_report'] or {},
            'max': formatted_min_max_report['max_report'] or {},
            'attribute_names': self._validation_report['metadata']['reference_metadata']['column_names'],
            'domain': self._validation_report['domain_test_results']
        }

    def serialized_output(self):
        import pickle
        return pickle.dumps(self.formatted_report())

    def _formatted_row_count_difference_report(self):
        default = {
            'expected_row_count': None,
            'actual_row_count': None,
            'row_count_diff': None
        }
        return self._validation_report.get('row_count', default)

    def _formatted_schema_report(self):
        if self._validation_report['schema_check_results']['passed']:
            all_details_by_attributes = self._attribute_details_for_all_columns_as_healthy()
            number_of_healthy_columns, _ = self._number_of_healthy_critical_columns()

            schema_report = {
                'summary': {
                    'healthy': number_of_healthy_columns,
                    'critical': 0,
                    'warning': 0
                },
                'details_by_attribute': self._sort_details_by_attribute(all_details_by_attributes)
            }
            
            return schema_report
        
        error_message = self._validation_report['schema_check_results']['error_message']
        if error_message == 'column sets not equal':
            schema_report = self._build_validation_report_for_column_sets_not_equal()
        elif error_message == 'columns not in order':
            schema_report = self._build_validation_report_for_columns_not_in_order()
        elif error_message == 'column datatype mismatches':
            schema_report = self._build_validation_report_for_datatype_mismatch()
        else:
            raise ValueError('Invalid error message')
        return schema_report

    
    def _number_of_healthy_critical_columns(self):
        columns_in_reference, columns_in_current = self._columns_in_dataframes()

        columns_in_reference = set(columns_in_reference)
        number_of_columns_in_reference = len(columns_in_reference)

        columns_in_current = set(columns_in_current)
        number_of_columns_in_current = len(columns_in_current)

        columns_in_common = columns_in_reference.intersection(columns_in_current)
        number_of_healthy_columns = len(columns_in_common)

        width_of_widest_dataframe = max(number_of_columns_in_current, number_of_columns_in_reference)
        number_of_critical_columns = width_of_widest_dataframe - number_of_healthy_columns

        return number_of_healthy_columns, number_of_critical_columns

    
    def _build_validation_report_for_column_sets_not_equal(self):
        number_of_healthy_columns, number_of_critical_columns = self._number_of_healthy_critical_columns()

        schema_report = {
            'summary': {
                'healthy': number_of_healthy_columns,
                'critical': number_of_critical_columns,
                'warning': 0
            }
        }

        missing_current_attribute_details = self._attribute_details_for_missing_columns('current')
        missing_reference_attribute_details = self._attribute_details_for_missing_columns('reference')
        missing_details_by_attribute = missing_current_attribute_details + missing_reference_attribute_details
        
        if missing_details_by_attribute:
            all_details_by_attributes = self._attribute_details_for_all_columns_as_healthy()
            healthy_details_by_attribute = self._healthy_columns_details(all_details_by_attributes, missing_details_by_attribute)
            final_details_by_attribute = list(healthy_details_by_attribute) + missing_details_by_attribute
            
            schema_report['details_by_attribute'] = self._sort_details_by_attribute(final_details_by_attribute)
        return schema_report

    def _build_validation_report_for_columns_not_in_order(self):
        columns_out_of_order = self._validation_report['schema_check_results']['columns_out_of_order']
        reference_column_names = self._validation_report['metadata']['reference_metadata']['column_names']
        number_of_columns_out_of_order = len(columns_out_of_order)
        number_of_columns = len(reference_column_names)

        schema_report = {
            'summary': {
                'healthy': number_of_columns - number_of_columns_out_of_order,
                'critical': number_of_columns_out_of_order,
                'warning': 0
            }
        }

        details_by_attribute = self._attribute_details_for_out_of_order_columns()
        if details_by_attribute:
            schema_report['details_by_attribute'] = details_by_attribute
        return schema_report

    def _build_validation_report_for_datatype_mismatch(self):
        columns_mismatched = self._validation_report['schema_check_results']['cols']
        reference_column_names = self._validation_report['metadata']['reference_metadata']['column_names']
        number_of_columns_mismatched = len(columns_mismatched)
        number_of_columns = len(reference_column_names)

        schema_report = {
            'summary': {
                'healthy': number_of_columns - number_of_columns_mismatched,
                'critical': number_of_columns_mismatched,
                'warning': 0
            }
        }

        details_by_attribute = self._attribute_details_for_mismatched_columns()
        if details_by_attribute:
            schema_report['details_by_attribute'] = details_by_attribute
        
        return schema_report

    @staticmethod
    def _sort_details_by_attribute(details_by_attribute):
        return sorted(details_by_attribute, key=lambda detail: (detail['validation_outcome'], detail['attribute_name']))

    def _healthy_columns_details(self, all_columns_details, error_columns_details):
        error_column_names = set(map(lambda column: column['attribute_name'], error_columns_details))
        for column in all_columns_details:
            if column['attribute_name'] not in error_column_names:
                yield column

    def _attribute_details_for_all_columns_as_healthy(self):
        type_mapping = self._validation_report['metadata']['current_metadata']['type_mapping']
        columns_in_current = self._columns_for_dataframe('current')
        details_for_attribute = []
        for column in columns_in_current:
            details_for_attribute.append({
                'attribute_name': column,
                'data_type': type_mapping[column],
                'issue_type': None,
                'validation_outcome': 'healthy'
            })
        return details_for_attribute

    def _attribute_details_for_missing_columns(self, column_type):
        missing_column_check = 'missing_in_ref' if column_type == 'reference' else 'missing_in_current'
        metadata = 'current_metadata' if column_type == 'reference' else 'reference_metadata'

        details_by_attribute = []
        missing_columns = self._validation_report['schema_check_results'][missing_column_check]
        type_mapping = self._validation_report['metadata'][metadata]['type_mapping']

        for missing_column in missing_columns:
            missing_data_type = type_mapping[missing_column]

            details_by_attribute.append({
                'attribute_name': missing_column,
                'data_type': missing_data_type,
                'issue_type': f'missing in {column_type} dataframe',
                'validation_outcome': 'critical'
            })

        return details_by_attribute

    def _attribute_details_for_out_of_order_columns(self):
        details_by_attribute = []

        type_mapping = self._validation_report['metadata']['reference_metadata']['type_mapping']
        columns_out_of_order = self._validation_report['schema_check_results']['columns_out_of_order']
        for column_out_of_order in columns_out_of_order:
            col_data_type = type_mapping[column_out_of_order]

            details_by_attribute.append({
                'attribute_name': column_out_of_order,
                'data_type': col_data_type,
                'issue_type': 'column is out of order',
                'validation_outcome': 'critical'
            })

        return details_by_attribute

    def _attribute_details_for_mismatched_columns(self):
        reference_type_mapping = self._validation_report['metadata']['reference_metadata']['type_mapping']
        current_type_mapping = self._validation_report['metadata']['current_metadata']['type_mapping']
        details_by_attribute = []

        columns_mismatched = self._validation_report['schema_check_results']['cols']
        for column_mismatched in columns_mismatched:
            details_by_attribute.append({
                'attribute_name': column_mismatched,
                'data_type': current_type_mapping[column_mismatched],
                'issue_type': f'datatype in reference dataframe is {reference_type_mapping[column_mismatched]}',
                'validation_outcome': 'critical'
            })
        return details_by_attribute

    def _formatted_data_quality_report(self):
        if not self._options.check_special_values:
            return None

        special_values = self._validation_report['special_values_check_results']


        data_quality_summary = {
            'healthy': 0,
            'critical': 0,
            'warning': 0
        }
        data_quality_attribute_details = []
        
        for col, col_results in special_values.items():
            for sv, sv_dict in col_results.items():
                attribute_details = dict()
                attribute_details["attribute_name"] = col
                attribute_details["value"] = str(sv)
                attribute_details["pct_in_reference_data"] = sv_dict['ref_percentage']
                attribute_details["pct_in_current_data"] = sv_dict['current_percentage']
                attribute_details["difference_in_pct"] = sv_dict['percentage_diff']
                attribute_details["validation_outcome"] = "healthy" if sv_dict["passed"] else "critical"
                data_quality_attribute_details.append(attribute_details)
                if sv_dict["passed"]:
                    data_quality_summary['healthy'] += 1
                else:
                    data_quality_summary['critical'] += 1

        return {
            'summary': data_quality_summary,
            'details_by_attribute': data_quality_attribute_details
        }
    
    def _formatted_population_shift_report(self):
        if not self._options.check_distribution:
            return None

        dist_check_results = self._validation_report['dist_check_results']
        
        population_shift_summary = {
            'healthy': 0,
            'critical': 0,
            'warning': 0
        }
        population_shift_attribute_details = []

        for column, col_results in dist_check_results.items():
            validation_outcome = None
            if col_results['binned_passed']:
                validation_outcome = 'healthy'
            elif col_results['binned_passed'] == False:
                validation_outcome = 'critical'

            details = {
                'attribute_name': column,
                'validation_outcome': validation_outcome
            }
            if 'binned_l_infinity' in col_results:
                details['L-infinity'] = col_results['binned_l_infinity']
            elif 'binned_psi' in col_results:
                details['PSI'] = col_results['binned_psi']
            population_shift_attribute_details.append(details)

            if col_results['binned_passed']:
                population_shift_summary['healthy'] += 1
            elif col_results['binned_passed'] == False:
                population_shift_summary['critical'] += 1

        return {
            'summary': population_shift_summary,
            'details_by_attribute': population_shift_attribute_details
        }

    def _formatted_min_max_report(self):
        if not self._options.check_min_max:
            return { 'min_report': {}, 'max_report': {} }

        min_max_check_results = self._validation_report['min_max_test_results']

        min_summary = {
            'healthy': 0,
            'critical': 0,
            'warning': 0
        }
        max_summary = {
            'healthy': 0,
            'critical': 0,
            'warning': 0
        }
        min_attribute_details = []
        max_attribute_details = []

        for column, col_results in min_max_check_results.items():
            for test_type, test_results in col_results.items():
                details = {
                    'attribute_name': column,
                    'validation_outcome': 'healthy' if test_results['passed'] else 'critical'
                }

                if test_type == 'min_test':
                    details['lower_bound'] = test_results['lower_bound']
                    details['min_value'] = test_results['min_value']
                    self._handle_min_max_test_health(test_results, details, min_summary)
                    min_attribute_details.append(details)
                elif test_type == 'max_test':
                    details['upper_bound'] = test_results['upper_bound']
                    details['max_value'] = test_results['max_value']
                    self._handle_min_max_test_health(test_results, details, max_summary)
                    max_attribute_details.append(details)
        return {
            'min_report': {
                'summary': min_summary,
                'details_by_attribute': min_attribute_details
            },
            'max_report': {
                'summary': max_summary,
                'details_by_attribute': max_attribute_details
            }
        }
    
    @staticmethod
    def _handle_min_max_test_health(test_results, details, summary_dict):
        if test_results['passed']:
            summary_dict['healthy'] += 1
        else:
            summary_dict['critical'] += 1
            details['percentage_out_of_bounds'] = test_results['percentage_out_of_bounds']

    def _columns_in_dataframes(self):
        columns_in_reference = self._columns_for_dataframe('reference')
        columns_in_current = self._columns_for_dataframe('current')

        return columns_in_reference, columns_in_current

    def _columns_for_dataframe(self, dataframe_name):
        report_metadata = self._validation_report['metadata']

        metadata = report_metadata[f'{dataframe_name}_metadata']
        return metadata['column_names']