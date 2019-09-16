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

        report = {
            'date': self._inference_period,
            'model_package': self._model_package,
            'data_contract': self._contract_name,
            'row_cnt_diff': row_cnt_diff
        }

        return report