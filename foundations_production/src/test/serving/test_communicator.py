"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.communicator import Communicator
import json

class TestCommunicator(Spec):

    @let
    def fake_data(self):
        return self.faker.sha1()
    
    mock_pipe = let_patch_mock('multiprocessing.Pipe')
    mock_master_pipe = let_mock()
    mock_worker_pipe = let_mock()

    @set_up
    def set_up(self):
        self.mock_pipe.return_value = (self.mock_master_pipe, self.mock_worker_pipe)
    
    def test_communicator_send_sends_data_to_client(self):
        Communicator().send_to_client(self.fake_data)
        self.mock_master_pipe.send.assert_called_with(json.dumps(self.fake_data))
    
    def test_communicator_send_sends_data_to_server(self):
        Communicator().send_to_server(self.fake_data)
        self.mock_worker_pipe.send.assert_called_with(json.dumps(self.fake_data))
    
    def test_communicator_receive_from_server_receives_data_from_server(self):
        self.mock_worker_pipe.recv.return_value = json.dumps(self.fake_data)
        data = Communicator().receive_from_server()

        self.assertEqual(self.fake_data, data)
    
    def test_communicator_receive_from_client_receives_data_from_client(self):
        self.mock_master_pipe.recv.return_value = json.dumps(self.fake_data)
        data = Communicator().receive_from_client()

        self.assertEqual(self.fake_data, data)