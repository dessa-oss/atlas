"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 02 2019
"""

from foundations_spec import *

import foundations
from foundations_contrib.global_state import config_manager

class TestJobUsesVenvCreatedByFoundations(Spec):

    @set_up
    def set_up(self):
        from scheduler_acceptance.cleanup import cleanup
        from foundations_contrib.cli.typed_config_listing import TypedConfigListing
        from foundations_scheduler_plugin.config.scheduler import translate

        cleanup()
        config_manager.push_config()
        TypedConfigListing('submission').update_config_manager_with_config('scheduler', translate)

    @tear_down
    def tear_down(self):
        config_manager.pop_config()

    def test_job_uses_virtualenv_created_by_foundations_when_running(self):
        from fnmatch import fnmatch

        job = foundations.submit(job_dir='acceptance/fixtures/virtual_environment')
        job.wait_for_deployment_to_complete()
        job_name = job.job_name()

        metrics_containing_python_path = foundations.get_metrics_for_all_jobs("virtual_environment")
        actual_python_path = self._get_python_path_from_metrics(metrics_containing_python_path, job_name)

        matches = fnmatch(actual_python_path, '/tmp/*/venv/bin/python')
        self.assertTrue(matches)

    @staticmethod
    def _get_python_path_from_metrics(metrics_containing_python_path, job_name):
        row_for_job = metrics_containing_python_path.loc[metrics_containing_python_path["job_id"] == job_name]
        return row_for_job.iloc[0]["python_path"]

