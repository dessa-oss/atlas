"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations import LocalShellJobDeployment

RESULT_SUCCESS = {
    "global_stage_context": {
        "error_information": None
    },
    'dummy_result': "dummy_result"
}

import sys
import traceback

try:
    1/0
except:
    error_info = sys.exc_info()
    RESULT_FAILURE = {
        "global_stage_context": {
            "error_information": {
                "type": error_info[0],
                "exception": error_info[1],
                "traceback": traceback.extract_tb(error_info[2])
            }
        },
        'dummy_result': "dummy_result"
    }


class MockDeployment(LocalShellJobDeployment):
    def __init__(self, *args, **kwargs):
        pass

class SuccessfulMockDeployment(MockDeployment):
    def is_job_complete(self):
        return True

    def fetch_job_results(self):
        result = RESULT_SUCCESS
        return result

class FailedMockDeployment(MockDeployment):
    def is_job_complete(self):
        return True

    def fetch_job_results(self):
        result = RESULT_FAILURE
        return result