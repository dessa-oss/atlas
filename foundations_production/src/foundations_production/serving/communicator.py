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

    def set_action_request(self, data_to_predict_on):
        self._master_pipe.send(json.dumps(data_to_predict_on))    

    def set_response(self, prediction):
        self._worker_pipe.send(json.dumps(prediction))

    def get_response(self):
        return json.loads(self._master_pipe.recv()) 

    def get_action_request(self):
        return json.loads(self._worker_pipe.recv()) 
    
    def close(self):
        self._master_pipe.close()
        self._worker_pipe.close()
    