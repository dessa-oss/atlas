"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import sys

class ErrorPrinter(object):
    """A class which provides functionality used for controlling error verbosity.
        Arguments:
            excepthook: {callback} -- The old exception hook.  Defaults to sys.__excepthook__.
    """

    def __init__(self, excepthook=sys.__excepthook__):
        from foundations.global_state import config_manager

        self._error_verbosity = config_manager.config().get("error_verbosity", "QUIET")
        self._excepthook = excepthook

    def traceback_string(self, ex_type, ex_value, ex_traceback):
        """Filters the stack trace (recursively, in the case of python 3) as defined by the error verbosity set in the config_manager.
            Arguments:
                ex_type: {type} -- The type of the exception to which the stack trace belongs.
                ex_value: {Exception} -- The exception value itself.
                ex_traceback: {TracebackType} -- The traceback for the exception.
        
        Returns:
            string -- A string representation of the filtered traceback, ready for output to stderr.
        """

        traceback_list = self._transformed_traceback_strings(ex_type, ex_value, ex_traceback)

        if ErrorPrinter._has_nested_exception(ex_value):
            inner_type, inner_value, inner_traceback, is_explicit = ErrorPrinter._get_inner_info(ex_value)
            inner_traceback_list = self._transformed_traceback_strings(inner_type, inner_value, inner_traceback)

            if is_explicit:
                separator = "\nThe above exception was the direct cause of the following exception:\n\n"
            else:
                separator = "\nDuring handling of the above exception, another exception occurred:\n\n"

            traceback_list = inner_traceback_list + [separator] + traceback_list

        return ErrorPrinter._concat(traceback_list)

    def get_callback(self):
        """Returns a callback for use in overriding sys.excepthook that filters the traceback in the same manner as traceback_string.

        Returns:
            callback -- As in the description.
        """

        def _callback(*args):
            import sys

            sys.stderr.write(self.traceback_string(*args))

        return _callback

    def get_old_excepthook(self):
        """Returns the old exception hook that was passed in.
        
        Returns:
            callback -- As in the description.
        """

        return self._excepthook

    def transform_extracted_traceback(self, extracted_traceback):
        """Lower-level utility for filtering a pre-extracted traceback.
            Arguments:
                extracted_traceback: {TracebackType} -- A pre-extracted traceback.

        Returns:
            transformed -- Filtered extracted traceback.
        """

        import traceback

        transform = self._get_transform()
        return transform(extracted_traceback)

    def _get_transform(self):
        if self._error_verbosity == "QUIET":
            return ErrorPrinter._quiet_traceback
        else:
            return ErrorPrinter._verbose_traceback

    @staticmethod
    def _get_inner_info(ex_value):
        if ex_value.__cause__ is not None:
            inner_exception = ex_value.__cause__
            is_explicit = True
        else:
            inner_exception = ex_value.__context__
            is_explicit = False

        return type(inner_exception), inner_exception, inner_exception.__traceback__, is_explicit

    @staticmethod
    def _quiet_traceback(traceback):
        return filter(ErrorPrinter._stack_trace_filter(), traceback)

    @staticmethod
    def _verbose_traceback(traceback):
        return traceback

    def _transformed_traceback_strings(self, ex_type, ex_value, ex_traceback):
        import traceback

        extracted_traceback = traceback.extract_tb(ex_traceback)
        cleaned_stack_trace = self.transform_extracted_traceback(extracted_traceback)

        header = ["Traceback (most recent call last):\n"]
        traceback_body = traceback.format_list(cleaned_stack_trace)
        exception_tail = traceback.format_exception_only(ex_type, ex_value)

        return header + traceback_body + exception_tail

    @staticmethod
    def _stack_trace_filter():
        from foundations.utils import get_foundations_root, check_is_in_dir
        foundations_root = get_foundations_root()

        def _is_disallowed(stack_file_name):
            return check_is_in_dir(foundations_root, stack_file_name) or stack_file_name == "main.py"

        def _filter_to_return(stack_info):
            stack_file_name = stack_info[0]
            return not _is_disallowed(stack_file_name)

        return _filter_to_return

    @staticmethod
    def _concat(list_of_strings):
        return "".join(list_of_strings)

    @staticmethod
    def _has_nested_exception(ex_value):
        import sys

        if sys.version_info.major < 3:
            return False

        return ex_value.__cause__ is not None or ex_value.__context__ is not None