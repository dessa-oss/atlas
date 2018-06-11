"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class RemoteException(Exception):
    def __init__(self, msg):
        super(RemoteException, self).__init__(msg)

def check_result(pipeline_name, result, verbose_errors=False):
    from vcat.compat import compat_raise
    from vcat.utils import pretty_error

    error_info = result["global_stage_context"]["error_information"]

    if error_info is None:
        return result
    else:
        compat_raise(RemoteException, pretty_error(pipeline_name, error_info, verbose_errors))