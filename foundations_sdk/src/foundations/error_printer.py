"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

from __future__ import print_function

class ErrorPrinter(object):
    def __init__(self):
        from foundations.global_state import config_manager

        self._error_verbosity = config_manager.config().get("error_verbosity", "QUIET")

    def printer_action(self):
        if self._error_verbosity == "QUIET":
            return ErrorPrinter._print_quietly
        else:
            return ErrorPrinter._print_verbosely

    @staticmethod
    def _print_quietly(ex_type, ex_value, ex_traceback):
        import sys
        import traceback

        extracted_traceback = traceback.extract_tb(ex_traceback)
        cleaned_stack_trace = filter(ErrorPrinter._stack_trace_filter(), extracted_traceback)

        to_print = ["Traceback (most recent call last):"]
        to_print += traceback.format_list(list(cleaned_stack_trace))
        to_print += traceback.format_exception_only(ex_type, ex_value)

        for line in to_print:
            print(line.rstrip('\n'), file=sys.stderr)
    
    @staticmethod
    def _print_verbosely(ex_type, ex_value, ex_traceback):
        import sys
        sys.__excepthook__(ex_type, ex_value, ex_traceback)

    @staticmethod
    def _stack_trace_filter():
        from foundations.utils import get_foundations_root, check_is_in_dir
        foundations_root = get_foundations_root()

        def _is_disallowed(stack_file_name):
            return check_is_in_dir(foundations_root, stack_file_name)

        def _filter_to_return(stack_info):
            stack_file_name = stack_info[0]
            return not _is_disallowed(stack_file_name)

        return _filter_to_return