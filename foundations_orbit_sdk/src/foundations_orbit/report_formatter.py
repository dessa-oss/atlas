"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ReportFormatter(object):

    def __init__(self, inference_period, model_package, contract_name, validation_report, options):
        self._inference_period = inference_period
        self._model_package = model_package
        self._contract_name = contract_name
        self._validation_report = validation_report
        self._options = options

    def formatted_report(self):
        return {
            'date': self._inference_period,
            'model_package': self._model_package,
            'data_contract': self._contract_name,
            'row_cnt_diff': self._formatted_row_count_difference_report(),
            'schema': self._formatted_schema_report()
        }

    def _formatted_row_count_difference_report(self):
        return self._validation_report.get('row_cnt_diff', 0)

    def _formatted_schema_report(self):
        columns_in_reference, columns_in_current = self._columns_in_dataframes()

        columns_in_reference = set(columns_in_reference)
        number_of_columns_in_reference = len(columns_in_reference)

        columns_in_current = set(columns_in_current)
        number_of_columns_in_current = len(columns_in_current)

        columns_in_common = columns_in_reference.intersection(columns_in_current)
        number_of_healthy_columns = len(columns_in_common)

        width_of_widest_dataframe = max(number_of_columns_in_current, number_of_columns_in_reference)
        number_of_critical_columns = width_of_widest_dataframe - number_of_healthy_columns

        schema_report = {
            'summary': {
                'healthy': number_of_healthy_columns,
                'critical': number_of_critical_columns
            }
        }
        if self._validation_report['schema_check_results']['passed']:
            return schema_report


        missing_current_attribute_details = self._attribute_details_for_missing_columns('current')
        missing_reference_attribute_details = self._attribute_details_for_missing_columns('reference')
        details_by_attribute = missing_current_attribute_details + missing_reference_attribute_details
        if details_by_attribute:
            schema_report['details_by_attribute'] = details_by_attribute

        return schema_report

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
                'issue_type': f'missing in {column_type}',
                'validation_outcome': 'error_state'
            })

        return details_by_attribute

    def _columns_in_dataframes(self):
        columns_in_reference = self._columns_for_dataframe('reference')
        columns_in_current = self._columns_for_dataframe('current')

        return columns_in_reference, columns_in_current

    def _columns_for_dataframe(self, dataframe_name):
        report_metadata = self._validation_report['metadata']

        metadata = report_metadata[f'{dataframe_name}_metadata']
        return metadata['column_names']