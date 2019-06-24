"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestLocalDeployWithoutStages(Spec):

    @skip('Not implemented yet')
    def test_stageless_project_deploys_succesfully(self):
        self._test_deploy_stageless_project('stageless-projects', 'stageless_project', 'driver.py')

    @skip('Not implemented yet')
    def test_stageless_project_with_nested_directory_deploys_succesfully(self):
        self._test_deploy_stageless_project('stageless-projects-nested', 'stageless_project_nested_project_code', 'project_code/driver.py')

    def _test_deploy_stageless_project(self, project_name, fixture_directory, driver_path):
        import subprocess

        change_to_fixture_directory_command = 'cd stageless_local_deployment/fixtures/{}'.format(fixture_directory)

        command_to_run = ["/bin/bash", "-c", "{} && python -m foundations deploy {} --env=local".format(change_to_fixture_directory_command, driver_path)]
        driver_deploy_completed_process = subprocess.run(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._assert_driver_completed_successfully(driver_deploy_completed_process)
        
        job_id = self._job_id_from_logs(driver_deploy_completed_process)

        command_for_retrieve_log = ["/bin/bash", "-c", "{} && python -m foundations retrieve logs --job_id={} --env=local".format(change_to_fixture_directory_command, job_id)]
        log_retrieve_process = subprocess.run(command_for_retrieve_log, stdout=subprocess.PIPE)

        self._assert_can_print(log_retrieve_process)
        self._assert_no_warning_printed(log_retrieve_process)

        self._assert_can_log_metrics(project_name, job_id)
        self._assert_can_set_tag(project_name, job_id)

    def _job_id_from_logs(self, driver_deploy_completed_process):
        import re

        logs_parsing_regex = re.compile("Job '(.*)' deployed")
        logs = self._driver_stdout(log_retrieve_process)
        return logs_parsing_regex.findall(logs)[0]

    def _assert_driver_completed_successfully(self, driver_deploy_completed_process):
        driver_stderr = driver_deploy_completed_process.stderr.decode()
        driver_return_code = driver_deploy_completed_process.returncode

        if driver_return_code != 0:
            raise AssertionError('Driver failed:\n{}'.format(driver_stderr))

    def _assert_can_print(self, log_retrieve_process):
        driver_stdout = self._driver_stdout(log_retrieve_process)
        self.assertIn('Hello World!', driver_stdout)

    def _assert_no_warning_printed(self, log_retrieve_process):
        driver_stdout = self._driver_stdout(log_retrieve_process)
        self.assertNotIn('Cannot log metric if not deployed with foundations deploy', driver_stdout)
        self.assertNotIn('Cannot set tag if not deployed with foundations deploy', driver_stdout)

    def _assert_can_log_metrics(self, project_name, job_id):
        self.assertEqual(84, self._get_logged_metric(project_name, job_id, 'Score'))
        self.assertEqual(42, self._get_logged_metric(project_name, job_id, 'Accuracy'))
        self.assertEqual(42, self._get_logged_metric(project_name, job_id, 'Cached_accuracy'))
    
    def _assert_can_set_tag(self, project_name, job_id):
        self.assertEqual(84, self._get_tag(project_name, job_id, 'Loss'))
    
    def _get_metrics_for_all_jobs(self, project_name):
        return foundations.get_metrics_for_all_jobs(project_name)

    def _get_logged_metric(self, project_name, job_id, metric_name):
        all_metrics = self._get_metrics_for_all_jobs(project_name)
        metrics_for_job = all_metrics.loc[all_metrics['job_id'] == job_id].iloc[0]
        return metrics_for_job[metric_name]
    
    def _get_tags_for_all_jobs(self, project_name):
        return foundations.prototype.get_metrics_for_all_jobs(project_name)

    def _get_tags_for_job(self, project_name, job_id):
        all_tags = self._get_tags_for_all_jobs(project_name)
        return all_tags.loc[all_tags['job_id'] == job_id].iloc[0]

    def _get_tag(self, project_name, job_id, tag):
        tags_for_job = self._get_tags_for_job(project_name, job_id)
        return tags_for_job['tag_{}'.format(tag)]

    def _driver_stdout(self, driver_deploy_completed_process):
        return driver_deploy_completed_process.stdout.decode()
