"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.restartable_process import RestartableProcess

class TestRestartableProcess(Spec):

    target = let_mock()
    mock_process_instance = let_mock()
    mock_process_instance_2 = let_mock()
    mock_communicator_instance = let_mock()
    mock_communicator_instance_2 = let_mock()
    mock_communicator = let_patch_mock('foundations_production.serving.communicator.Communicator')

    @let
    def args(self):
        return tuple(self.faker.words())

    @let
    def kwargs(self):
        return self.faker.pydict()

    @set_up
    def set_up(self):
        self.mock_process = self.patch('multiprocessing.Process', ConditionalReturn())
        self.mock_process.return_when(self.mock_process_instance, target=self.target, args=(self.args + (self.mock_communicator_instance,)), kwargs=self.kwargs, daemon=True)
        self.mock_process.return_when(self.mock_process_instance_2, target=self.target, args=(() + (self.mock_communicator_instance,)), kwargs={}, daemon=True)
        self.restartable_process = RestartableProcess(self.target, self.args, self.kwargs)
        self.mock_communicator.side_effect = [self.mock_communicator_instance, self.mock_communicator_instance_2]

    def test_start_restartable_process_starts_process(self):
        self.restartable_process.start()
        self.mock_process_instance.start.assert_called()
    
    def test_start_returns_communicator(self):
        actual_communicator = self.restartable_process.start()
        self.assertEqual(self.mock_communicator_instance, actual_communicator)
    
    def test_terminate_closes_communicator(self):
        self.restartable_process.start()
        self.restartable_process.terminate()
        self.mock_communicator_instance.close.assert_called()
    
    def test_terminate_terminates_process(self):
        self.restartable_process.start()
        self.restartable_process.terminate()
        self.mock_process_instance.terminate.assert_called()

    def test_terminate_terminates_only_once(self):
        self.restartable_process.start()
        self.restartable_process.terminate()
        self.restartable_process.terminate()
        self.mock_process_instance.terminate.assert_called_once()

    def test_terminate_starts_only_once(self):
        self.restartable_process.start()
        self.restartable_process.start()
        self.mock_process_instance.start.assert_called_once()
    
    def test_start_returns_existing_communicator_if_process_already_started(self):
        self.restartable_process.start()
        communicator = self.restartable_process.start()
        self.assertEqual(self.mock_communicator_instance, communicator)
    
    def test_restartable_process_has_default_args_and_kwargs(self):
        RestartableProcess(self.target).start()
        self.mock_process_instance_2.start.assert_called()
