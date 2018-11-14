"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""


class ThreadManager(object):

    def __init__(self, serial=False):
        import os
        
        is_running_2_7_on_jenkins = os.environ.get('PY_27_JENKINS', 'False') == 'True'
        self._pool = []
        self._serial = is_running_2_7_on_jenkins or serial

    def __enter__(self):
        return self

    def __exit__(self, *args):
        from foundations.helpers.future import Future

        Future.all(self._pool).get()

    def spawn(self, target, *args, **kwargs):
        from foundations.helpers.future import Future

        if self._serial:
            target(*args, **kwargs)
        else:
            self._pool.append(Future.execute(target, *args, **kwargs))
