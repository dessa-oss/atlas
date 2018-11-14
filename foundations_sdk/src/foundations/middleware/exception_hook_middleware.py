"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import sys

class ExceptionHookMiddleware(object):
    def __init__(self):
        from foundations.error_printer import ErrorPrinter

        self._error_printer = ErrorPrinter(sys.__excepthook__)

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        sys.excepthook = self._error_printer.get_callback()

        callback_result = callback(args, kwargs)

        sys.excepthook = self._error_printer.get_old_excepthook()
        return callback_result