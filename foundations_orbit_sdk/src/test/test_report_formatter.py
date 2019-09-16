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
    def validation_report(self):
        return {}

    @let
    def row_count_diff(self):
        return self.faker.random.random()

    def test_report_formatter_returns_formatted_report_with_expected_date(self):
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.inference_period, formatted_report['date'])

    def test_report_formatter_returns_formatted_report_with_expected_model_package(self):
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.model_package, formatted_report['model_package'])

    def test_report_formatter_returns_formatted_report_with_expected_data_contract(self):
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.contract_name, formatted_report['data_contract'])

    def test_report_formatter_returns_formatted_report_with_expected_row_cnt_diff_if_does_not_exist(self):
        formatted_report = self._generate_formatted_report()
        self.assertEqual(0, formatted_report['row_cnt_diff'])

    def test_report_formatter_returns_formatted_report_with_expected_row_cnt_diff_if_exist(self):
        self.validation_report['row_cnt_diff'] = self.row_count_diff
        formatted_report = self._generate_formatted_report()
        self.assertEqual(self.row_count_diff, formatted_report['row_cnt_diff'])

    def _generate_formatted_report(self):
        formatter = ReportFormatter(inference_period=self.inference_period,
                                    model_package=self.model_package,
                                    contract_name=self.contract_name,
                                    validation_report=self.validation_report,
                                    options=Mock())

        return formatter.formatted_report()