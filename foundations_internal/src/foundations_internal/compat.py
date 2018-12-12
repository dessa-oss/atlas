"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import sys

if sys.version_info.major == 3:
    def compat_raise(exception_type, message, traceback=None):
        if traceback:
            raise exception_type(message).with_traceback(traceback)
        else:
            raise exception_type(message)
else:
    python_2_raise  = "def compat_raise(exception_type, message, traceback=None):\n"
    python_2_raise += "    if traceback:\n"
    python_2_raise += "        raise exception_type, message, traceback\n"
    python_2_raise += "    else:\n"
    python_2_raise += "        raise exception_type, message\n"

    exec(python_2_raise)

def make_queue():
    if sys.version_info.major == 3:
        import queue
        return queue.Queue()
    else:
        import Queue
        return Queue.Queue()
