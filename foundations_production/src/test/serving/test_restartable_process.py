"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.restartable_process import RestartableProcess

class TestRestartableProcess(Spec):
    @let
    def args(self):
        return tuple(self.faker.words())

    @let
    def kwargs(self):
        return self.faker.pydict()

    target = let_mock()
    mock_process_instance = let_mock()
    connection_worker_pipe = let_mock()
    connection_master_pipe = let_mock()
    mock_pipe = let_patch_mock('multiprocessing.Pipe')

    @set_up
    def set_up(self):
        self.mock_process = self.patch('multiprocessing.Process', ConditionalReturn())
        self.mock_process.return_when(self.mock_process_instance, target=self.target, args=(self.args + (self.connection_worker_pipe,)), kwargs=self.kwargs, daemon=True)

        self.mock_pipe.return_value = (self.connection_master_pipe, self.connection_worker_pipe)

    def test_start_restartable_process_starts_process(self):
        RestartableProcess(self.target, self.args, self.kwargs).start()
        self.mock_process_instance.start.assert_called()
    
    def test_start_returns_master_end_of_pipe(self):
        actual_pipe = RestartableProcess(self.target, self.args, self.kwargs).start()
        self.assertEqual(self.connection_master_pipe, actual_pipe)

