"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DataContractSummary(object):

    def __init__(self, formatted_validation_report):
        self._num_critical_tests = 0
        self._report = formatted_validation_report
        self._tests_to_summarize = ['schema', 'data_quality', 'population_shift', 'min', 'max']
        self.summarize_report()

    def summarize_report(self):
        for test in self._tests_to_summarize:
            if self._report[test]['summary']['critical'] > 0:
                self._num_critical_tests += 1

    def serialized_output(self):
        import pickle

        data_contract_summary = {
            'num_critical_tests': self._num_critical_tests
        }
        return pickle.dumps(data_contract_summary)