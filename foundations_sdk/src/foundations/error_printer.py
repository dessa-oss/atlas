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

    def traceback_string(self, ex_type, ex_value, ex_traceback):
        traceback_list = self._pretty_print(ex_type, ex_value, ex_traceback)

        if ErrorPrinter._has_nested_exception(ex_value):
            inner_type, inner_value, inner_traceback = ErrorPrinter._get_inner_info(ex_value)
            inner_traceback_list = self._pretty_print(inner_type, inner_value, inner_traceback)
            separator = ["\nDuring handling of the above exception, another exception occurred:\n\n"]
            traceback_list = inner_traceback_list + separator + traceback_list

        return ErrorPrinter._concat(traceback_list)

    def _pretty_print(self, ex_type, ex_value, ex_traceback):
        if self._error_verbosity == "QUIET":
            pretty_printer = ErrorPrinter._quiet_traceback_strings
        else:
            pretty_printer = ErrorPrinter._verbose_traceback_strings

        return pretty_printer(ex_type, ex_value, ex_traceback)

    @staticmethod
    def _get_inner_info(ex_value):
        inner_exception = ex_value.__context__
        return type(inner_exception), inner_exception, inner_exception.__traceback__

    @staticmethod
    def _quiet_traceback_strings(ex_type, ex_value, ex_traceback):
        import traceback

        extracted_traceback = traceback.extract_tb(ex_traceback)
        cleaned_stack_trace = filter(ErrorPrinter._stack_trace_filter(), extracted_traceback)

        header = ["Traceback (most recent call last):\n"]
        traceback_body = traceback.format_list(cleaned_stack_trace)
        exception_tail = traceback.format_exception_only(ex_type, ex_value)

        return header + traceback_body + exception_tail

    @staticmethod
    def _verbose_traceback_strings(ex_type, ex_value, ex_traceback):
        import traceback
        
        list_of_traceback_strings = traceback.format_exception(ex_type, ex_value, ex_traceback)
        return list_of_traceback_strings

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

    @staticmethod
    def _concat(list_of_strings):
        return "".join(list_of_strings)

    @staticmethod
    def _has_nested_exception(ex_value):
        return "__context__" in dir(ex_value) and ex_value.__context__ is not None