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

    def test_fail(self):
        from acceptance.fixtures.stages import path_check

        foundations.set_project_name("version-check-test")

        path_check = foundations.create_stage(path_check)

        path_check_job = path_check().run()
        job_name = path_check_job.job_name()

        path_check_job.wait_for_deployment_to_complete()

        metrics_containing_python_path = foundations.get_metrics_for_all_jobs("version-check-test")

        actual_python_path = _get_python_path_from_metrics(metrics_containing_python_path, job_name)
        expected_python_path = _get_python_path(job_name)

        self.assertEqual(expected_python_path, actual_python_path)

def _get_python_path_from_metrics(metrics_containing_python_path, job_name):
    row_for_job = metrics_containing_python_path.loc[metrics_containing_python_path["job_id"] == job_name]
    return row_for_job.iloc[0]["python_path"]

def _get_python_path(job_name):
    from os import getcwd
    from os.path import join

    parent_directory = getcwd()
    return join(parent_directory, job_name, "venv", "bin", "python")