"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 02 2019
"""

import unittest

import foundations

class TestJobUsesVenvCreatedByFoundations(unittest.TestCase):

    def setUp(self):
        from acceptance.cleanup import cleanup

        cleanup()

    def test_job_uses_virtualenv_created_by_foundations_when_running(self):
        from acceptance.fixtures.stages import get_and_log_python_path_as_metric
        from fnmatch import fnmatch

        foundations.set_project_name("version-check-test")

        get_and_log_python_path_as_metric_stage = foundations.create_stage(get_and_log_python_path_as_metric)

        get_and_log_python_path_as_metric_job = get_and_log_python_path_as_metric_stage().run()
        job_name = get_and_log_python_path_as_metric_job.job_name()

        get_and_log_python_path_as_metric_job.wait_for_deployment_to_complete()

        metrics_containing_python_path = foundations.get_metrics_for_all_jobs("version-check-test")

        actual_python_path = self._get_python_path_from_metrics(metrics_containing_python_path, job_name)

        matches = fnmatch(actual_python_path, '/tmp/*/venv/bin/python')
        self.assertTrue(matches)

    @staticmethod
    def _get_python_path_from_metrics(metrics_containing_python_path, job_name):
        row_for_job = metrics_containing_python_path.loc[metrics_containing_python_path["job_id"] == job_name]
        return row_for_job.iloc[0]["python_path"]

