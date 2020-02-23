

from foundations_spec import *

from foundations.submission import submit

class TestSubmit(Spec):

    random_parameter = let_mock()
    mock_submit = let_patch_mock('foundations_core_cli.job_submission.submit_job.submit')
    mock_push_state = let_patch_mock('foundations_contrib.global_state.push_state')
    mock_pop_state = let_patch_mock('foundations_contrib.global_state.pop_state')

    @set_up
    def set_up(self):
        self.mock_submit.side_effect = self._set_value
        self._arguments = None
    
    def test_submit_passes_scheduler_config_name(self):
        submit(scheduler_config=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.scheduler_config)

    def test_submit_passes_job_dir(self):
        submit(job_directory=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.job_directory)

    def test_submit_passes_project_name(self):
        submit(project_name=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.project_name)

    def test_submit_passes_entrypoint(self):
        submit(entrypoint=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.entrypoint)

    def test_submit_passes_params(self):
        submit(params=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.params)

    def test_submit_passes_ram(self):
        submit(ram=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.ram)

    def test_submit_passes_num_gpus(self):
        submit(num_gpus=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.num_gpus)

    def test_submit_passes_stream_job_logs_option(self):
        submit(stream_job_logs=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.stream_job_logs)

    def test_submit_passes_command_option(self):
        submit(command=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.command)

    def test_submit_is_accessible_globally(self):
        import foundations
        self.assertEqual(submit, foundations.submit)

    def test_submit_pushes_global_state(self):
        submit()
        self.mock_push_state.assert_called()

    def test_submit_pops_global_state(self):
        submit()
        self.mock_pop_state.assert_called()

    def test_submit_pops_global_state_even_when_an_error_happens(self):
        self.mock_submit.side_effect = self._die
        with self.assertRaises(Exception):
            submit()
        self.mock_pop_state.assert_called()

    def _die(self, *args):
        raise Exception('It died')

    def _set_value(self, arguments):
        self._arguments = arguments