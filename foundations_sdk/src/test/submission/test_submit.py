"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""


from foundations_spec import *

from foundations.submission import submit

class TestSubmit(Spec):

    random_parameter = let_mock()
    mock_submit = let_patch_mock('foundations_contrib.cli.job_submission.submit_job.submit')

    @set_up
    def set_up(self):
        self.mock_submit.side_effect = self._set_value
        self._arguments = None
    
    def test_submit_passes_scheduler_config_name(self):
        submit(scheduler_config=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.scheduler_config)

    def test_submit_passes_job_dir(self):
        submit(job_dir=self.random_parameter)
        self.assertEqual(self.random_parameter, self._arguments.job_dir)

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

    def test_submit_is_accessible_globally(self):
        import foundations
        self.assertEqual(submit, foundations.submit)

    def _set_value(self, arguments):
        self._arguments = arguments