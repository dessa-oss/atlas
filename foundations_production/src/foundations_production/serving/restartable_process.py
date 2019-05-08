"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class RestartableProcess(object):
    
    def __init__(self, target, args, kwargs):
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._master_pipe = None
        self._process = None
    
    def start(self):
        from multiprocessing import Process, Pipe

        master_pipe, worker_pipe = Pipe()
        self._master_pipe = master_pipe
        process = Process(target=self._target, args=(self._args + (worker_pipe,)), kwargs=self._kwargs, daemon=True)
        self._process = process
        process.start()
        return master_pipe
    
    def close(self):

        self._master_pipe.close()
        self._process.close()
