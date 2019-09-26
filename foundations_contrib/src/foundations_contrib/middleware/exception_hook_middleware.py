"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import sys


class ExceptionHookMiddleware(object):
    def __init__(self):
        self._error = sys.__excepthook__

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):

        self._log().error(self._error)

        callback_result = callback(args, kwargs)

        sys.excepthook = self._error
        return callback_result

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__) 