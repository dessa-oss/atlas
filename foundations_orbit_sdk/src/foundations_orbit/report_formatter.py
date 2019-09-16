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
        row_cnt_diff = self._validation_report.get('row_cnt_diff', 0)

        number_of_columns_in_reference, number_of_columns_in_current = self._number_of_columns_in_dataframes()

        if number_of_columns_in_reference <= number_of_columns_in_current:
            number_of_healthy_columns = number_of_columns_in_reference
        else:
            number_of_healthy_columns = number_of_columns_in_current

        if number_of_columns_in_current == number_of_columns_in_reference:
            number_of_critical_columns = 0
        else:
            number_of_critical_columns = 1

        report = {
            'date': self._inference_period,
            'model_package': self._model_package,
            'data_contract': self._contract_name,
            'row_cnt_diff': row_cnt_diff,
            'schema': {
                'summary': {
                    'healthy': number_of_healthy_columns,
                    'critical': number_of_critical_columns
                }
            }
        }

        return report

    def _number_of_columns_in_dataframes(self):
        number_of_columns_in_reference = self._number_of_columns_for_dataframe('reference')
        number_of_columns_in_current = self._number_of_columns_for_dataframe('current')

        return number_of_columns_in_reference, number_of_columns_in_current

    def _number_of_columns_for_dataframe(self, dataframe_name):
        report_metadata = self._validation_report['metadata']

        metadata = report_metadata[f'{dataframe_name}_metadata']
        column_names = metadata['column_names']
        return len(column_names)