"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class RemoteException(Exception):
    def __init__(self, msg):
        super(RemoteException, self).__init__(msg)


def check_result(pipeline_name, result):
    import sys

    from foundations_internal.compat import compat_raise
    from foundations.utils import pretty_error

    error_info = (result or {}).get("global_stage_context", {}).get("error_information", None)

    if error_info is None:
        return result
    else:
        error_message, callback = pretty_error(pipeline_name, error_info)
        sys.excepthook = callback
        compat_raise(RemoteException, error_message)
