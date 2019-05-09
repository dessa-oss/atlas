"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import json

class Communicator(object):

    def __init__(self):
        from multiprocessing import Pipe

        master_pipe, worker_pipe = Pipe()
        self._master_pipe = master_pipe
        self._worker_pipe = worker_pipe

    def send_to_client(self, data):
        self._master_pipe.send(json.dumps(data))    

    def send_to_server(self, data):
        self._worker_pipe.send(json.dumps(data))

    def receive_from_client(self):
        return json.loads(self._master_pipe.recv()) 
        
    def receive_from_server(self):
        return json.loads(self._worker_pipe.recv()) 
    