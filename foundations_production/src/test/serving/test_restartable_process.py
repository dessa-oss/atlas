"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestRestartableProcess(Spec):
    @let
    def args(self):
        return tuple(self.faker.words())

    @let
    def kwargs(self):
        return self.faker.pydict()

    target = let_mock()
    mock_pipe = let_patch_mock('multiprocessing.Pipe')

    def test_start_restartable_process_starts_process(self):
        from foundations_production.serving.restartable_process import RestartableProcess

        mock_process = self.patch('multiprocessing.Process', ConditionalReturn())
        mock_process_instance = Mock()
        connection_worker_pipe = Mock()
        connection_master_pipe = Mock()

        self.mock_pipe.return_value = (connection_master_pipe, connection_worker_pipe)
        mock_process.return_when(mock_process_instance, target=self.target, args=(self.args + (connection_worker_pipe,)), kwargs=self.kwargs, daemon=True)

        restartable_process = RestartableProcess(self.target, self.args, self.kwargs).start()

        mock_process_instance.start.assert_called()
