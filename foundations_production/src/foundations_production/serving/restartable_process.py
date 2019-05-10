"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class RestartableProcess(object):
    
    def __init__(self, target, args=(), kwargs={}):
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._communicator = None
        self._process = None
    
    def start(self):
        from multiprocessing import Process
        from foundations_production.serving.communicator import Communicator

        if not self._process:
            self._communicator = Communicator()
            process_spawn_arguments = (*self._args, self._communicator)
            self._process = Process(target=self._target, args=process_spawn_arguments, kwargs=self._kwargs, daemon=True)
            self._process.start()
            
        return self._communicator
    
    def close(self):
        if self._process is not None:
            self._communicator.close()
            self._process.close()

        self._process = None
        self._communicator = None
