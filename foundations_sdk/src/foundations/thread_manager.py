"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""

import threading

class ThreadManager(object):
    def __init__(self):
        self._pool = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for thread in self._pool:
            thread.join()

    def spawn(self, target, *args, **kwargs):
        thread = threading.Thread(target=target, args=args, kwargs=kwargs)
        self._pool.append(thread)
        thread.start()