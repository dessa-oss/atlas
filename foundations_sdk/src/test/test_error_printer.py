"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

from foundations.error_printer import ErrorPrinter
from foundations import config_manager, create_stage
import test.fixtures.stages as stages

class TestErrorPrinter(unittest.TestCase):
    def setUp(self):
        config_manager.config().pop("error_verbosity", None)

    def test_traceback_string_verbose_run_same_process(self):
        config_manager["error_verbosity"] = "VERBOSE"
        bad_job = TestErrorPrinter._create_bad_job()
        self._base_test(bad_job, no_alter=True)

    def test_traceback_string_quiet_run_same_process(self):
        config_manager["error_verbosity"] = "QUIET"
        bad_job = TestErrorPrinter._create_bad_job()
        self._base_test(bad_job)

    def test_traceback_string_default_quiet_run_same_process(self):
        bad_job = TestErrorPrinter._create_bad_job()
        self._base_test(bad_job)

    def test_traceback_string_two_stages_first_fails(self):
        divide_by_zero = create_stage(stages.divide_by_zero)
        make_data = create_stage(stages.make_data)

        oh_no = divide_by_zero()
        data = make_data(oh_no)

        self._base_test(data)

    def test_traceback_string_two_stages_second_fails(self):
        make_data = create_stage(stages.make_data)
        divide_by_zero = create_stage(lambda data: stages.divide_by_zero())

        data = make_data()
        oh_no = divide_by_zero(data)

        self._base_test(oh_no)

    def test_traceback_string_third_party(self):
        import pandas as pd

        empty_dataframe = create_stage(stages.empty_dataframe)
        illegal_access = create_stage(stages.get_asdf)

        df = empty_dataframe()
        rip = illegal_access(df)

        self._base_test(rip)

    def test_implicit_chained_exception(self):
        implicit = create_stage(stages.implicit_chained_exception)
        self._base_test(implicit)

    def test_explicit_chained_exception(self):
        explicit = create_stage(stages.explicit_chained_exception)
        self._base_test(explicit)

    # def test_

    @staticmethod
    def _create_bad_job():
        return create_stage(stages.divide_by_zero)()

    def _base_test(self, job_to_run, no_alter=False, debug=False):
        if no_alter:
            string_list_transform = lambda list_of_strings: list_of_strings
        else:
            string_list_transform = TestErrorPrinter._filter_out_foundations

        try:
            job_to_run.run_same_process()
        except:
            import sys
            import traceback

            ex_type, ex_value, ex_traceback = sys.exc_info()

            raw = traceback.format_exception(ex_type, ex_value, ex_traceback)

            expected_result = string_list_transform(raw)
            actual_result = ErrorPrinter().traceback_string(ex_type, ex_value, ex_traceback)

            self.assertEqual(actual_result, "".join(expected_result))

    @staticmethod
    def _filter_out_foundations(traceback_string_list):
        from foundations.utils import get_foundations_root
        foundations_root = get_foundations_root()

        def _is_not_foundations(string):
            return foundations_root not in string

        return filter(_is_not_foundations, traceback_string_list)