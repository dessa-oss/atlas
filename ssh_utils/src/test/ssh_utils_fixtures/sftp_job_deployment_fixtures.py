
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

