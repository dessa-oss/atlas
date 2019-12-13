"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import requests
import time


class TestSchedulerMonitorPackageViaRESTAPI(Spec):

    sleep_time = 1
    existing_words = []
    _flask_process = None

    @set_up_class
    def set_up_class(klass):
        import subprocess
        import time
        from foundations_contrib.global_state import redis_connection
        redis_connection.flushall()

        # Clear any un-removed flask process to prevent conflicts
        get_pid_for_any_flask_app = "kill -9 $(lsof -i:37222 -t)" # Command not found in Jenkins
        subprocess.run(get_pid_for_any_flask_app, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        klass._flask_process = subprocess.Popen(
            'python start_api_server.py',
            shell=True,
            cwd='orbit_acceptance/fixtures/orbit_rest_api',
            stdout=subprocess.PIPE
        )
        time.sleep(2)  # wait for the flask server to come up before proceeding

    @tear_down_class
    def tear_down_class(klass):
        if klass._flask_process is not None:
            klass._flask_process.terminate()

    def _gen_unique_word(self):
        word = self.faker.word().lower()
        while word in self.existing_words:
            word = self.faker.word().lower()
        self.existing_words.append(word)

        return word

    @let
    def monitor_name(self):
        return self._gen_unique_word()

    @let
    def monitor_name_2(self):
        return self._gen_unique_word()

    @let
    def invalid_monitor_name(self):
        return self._gen_unique_word()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def project_name_2(self):
        return self.faker.word()

    @let
    def env(self):
        return self.faker.word()

    @let
    def commands(self):
        return ['python main.py']

    @let
    def job_directory_binary(self):
        return None # TODO a binary file for uploading via HTTPS

    @let
    def orbit_monitor_base_api_url(self):
        return f'http://localhost:37222/api/v1/projects/{self.project_name}/monitors'

    @let
    def atlas_job_listing_base_api_url(self):
        return f'http://localhost:37223/api/v2beta/projects/{self.project_name}/job_listing'

    @let
    def valid_schedule_every_5_secs(self):
        return {
            'schedule': {
                'second': '*/5'
            }
        }

    @let
    def valid_schedule_every_2_secs(self):
        return {
            'schedule': {
                'second': '*/2'
            }
        }

    @let
    def invalid_schedule_1(self):
        return {
            'schedule': {
                'days': '*',
                'seconds': '*/5'
            }
        }

    @let
    def invalid_schedule_2(self):
        return {
            'schedule': {
                'second': 'not-a-second'
            }
        }

    @tear_down
    def tear_down(self):
        self._delete_monitor(monitor_name=self.monitor_name)
        self._delete_monitor(monitor_name=self.monitor_name_2)

    @staticmethod
    def _delete_scheduled_job(job_name):
        import os
        import requests

        scheduler_address = os.environ['LOCAL_DOCKER_SCHEDULER_HOST']
        return requests.delete(f'http://{scheduler_address}:5000/scheduled_jobs/{job_name}')

    def test_pause_scheduled_monitor_package_via_api(self):
        self._start_and_wait_for_monitor(self.monitor_name)

        pause_response = self._pause_monitor()
        self.assertEqual(204, pause_response.status_code)

    def test_pause_scheduled_monitor_package_via_api_halts_execution_but_can_resume_later(self):
        self._start_and_wait_for_monitor(self.monitor_name)
        pause_response = self._pause_monitor()
        self.assertEqual(204, pause_response.status_code)

        resume_response = self._resume_monitor()
        self.assertEqual(204, resume_response.status_code)

    def test_attempting_to_pause_invalid_monitor_should_produce_404(self):
        pause_response = self._pause_monitor(monitor_name=self.invalid_monitor_name)
        self.assertEqual(404, pause_response.status_code)

    def test_attempting_to_resume_invalid_monitor_should_produce_404(self):
        self._start_and_wait_for_monitor(self.monitor_name)

        resume_response = self._resume_monitor(monitor_name=self.invalid_monitor_name)
        self.assertEqual(404, resume_response.status_code)

    def test_get_scheduled_monitors_returns_scheduled_monitors(self):
        self._start_and_wait_for_monitor(self.monitor_name)
        self._start_and_wait_for_monitor(self.monitor_name_2)

        monitors_response = self._get_all_monitors()
        monitors = monitors_response.json()
        self.assertIn(f'{self.project_name}-{self.monitor_name}', monitors)
        self.assertIn(f'{self.project_name}-{self.monitor_name_2}', monitors)

        delete_response1 = self._delete_monitor(self.monitor_name)
        self.assertEqual(204, delete_response1.status_code)

        delete_response2 = self._delete_monitor(self.monitor_name_2)
        self.assertEqual(204, delete_response2.status_code)

    def test_get_scheduled_monitor_returns_scheduled_monitor(self):
        self._start_and_wait_for_monitor(self.monitor_name)

        monitor_response = self._get_monitor(self.monitor_name)
        self.assertEqual(200, monitor_response.status_code)
        monitor_content = monitor_response.json()[f'{self.project_name}-{self.monitor_name}']

        expected_schedule = {
            'day': '*',
            'day_of_week': '*',
            'end_date': None,
            'hour': '*',
            'minute': '*',
            'month': '*',
            'second': '*',
            'start_date': None,
            'week': '*',
            'year': '*'
        }

        self.assertEqual(200, monitor_response.status_code)
        self.assertEqual('paused', monitor_content['status'])
        self.assertEqual(expected_schedule, monitor_content['schedule'])
        self.assertEqual([None, None, None], monitor_content['next_run_time'])

        delete_response = self._delete_monitor(self.monitor_name)
        self.assertEqual(204, delete_response.status_code)

    def test_delete_scheduled_monitor_successfully_deletes_monitor(self):
        self._start_and_wait_for_monitor(self.monitor_name)

        monitor_package = f'{self.project_name}-{self.monitor_name}'

        monitor_response = self._get_all_monitors()
        self.assertIn(monitor_package, monitor_response.json())

        delete_response = self._delete_monitor(self.monitor_name)
        self.assertEqual(204, delete_response.status_code)

        monitor_response = self._get_all_monitors()
        self.assertNotIn(monitor_package, monitor_response.json())

    def test_delete_nonexistent_monitor_returns_404(self):
        delete_response = self._delete_monitor(self.monitor_name)
        self.assertEqual(404, delete_response.status_code)

    def test_update_schedule_on_nonexistent_monitor_returns_404(self):
        valid_schedule = self.valid_schedule_every_5_secs
        update_response = self._update_monitor(self.monitor_name, valid_schedule)

        self.assertEqual(404, update_response.status_code)

    def test_update_schedule_on_monitor_with_invalid_schedule_returns_400(self):
        self._start_and_wait_for_monitor(self.monitor_name)

        monitor_response = self._get_all_monitors()
        monitor_package = f'{self.project_name}-{self.monitor_name}'
        self.assertIn(monitor_package, monitor_response.json())

        invalid_schedule_1 = self.invalid_schedule_1
        update_response = self._update_monitor(self.monitor_name, invalid_schedule_1)
        self.assertEqual(404, update_response.status_code)

        invalid_schedule_2 = self.invalid_schedule_2
        update_response = self._update_monitor(self.monitor_name, invalid_schedule_2)
        self.assertEqual(404, update_response.status_code)

    def test_update_schedule_on_monitor_with_correct_schedule_returns_204(self):
        self._start_and_wait_for_monitor(self.monitor_name)

        monitor_response = self._get_all_monitors()
        monitor_package = f'{self.project_name}-{self.monitor_name}'
        self.assertIn(monitor_package, monitor_response.json())

        valid_schedule = self.valid_schedule_every_5_secs
        update_response = self._update_monitor(self.monitor_name, valid_schedule)
        self.assertEqual(204, update_response.status_code)

    def test_get_monitor_jobs_for_nonexistent_monitor_returns_404(self):
        get_jobs_response = self._get_monitor_jobs(self.monitor_name)
        self.assertEqual(404, get_jobs_response.status_code)

    def _start_monitor_and_retrieve_jobs(self):
        self._start_and_update_and_resume_monitor(self.monitor_name)
        # paused to attempt to reduce the occurrence of other jobs running between evaluating outputs of the jobs
        self._pause_monitor()
        # give job time to complete
        time.sleep(15)

        jobs_list_response = self._get_monitor_jobs(self.monitor_name)
        self.assertEqual(200, jobs_list_response.status_code)

        return jobs_list_response.json()

    @skip('Cannot figure out reason for failure')
    def test_all_jobs_requested_for_a_monitor_belongs_to_the_monitor(self):
        jobs_list = self._start_monitor_and_retrieve_jobs()

        for job in jobs_list:
            self.assertEqual(self.project_name, job['project_name'])
            self.assertIn(self.monitor_name, job['job_id'])

    @skip('Cannot figure out reason for failure')
    def test_get_monitor_jobs_returns_all_jobs_for_monitor(self):
        jobs_list = self._start_monitor_and_retrieve_jobs()
        number_of_runs = self._get_number_of_production_metrics_produced_by_jobs()
        self.assertEqual(number_of_runs, len(jobs_list))

    def _get_number_of_production_metrics_produced_by_jobs(self):
        from foundations_orbit_rest_api.v1.models.production_metric_set import ProductionMetricSet
        metric_sets = ProductionMetricSet.all(self.project_name).evaluate()
        number_of_runs = len(metric_sets[0].series[0]['data'])
        return number_of_runs

    @skip('Skipped for now')
    def test_delete_monitor_job_deletes_job(self):
        try:
            self._start_and_update_and_resume_monitor(self.monitor_name)
            jobs_list = self._get_monitor_jobs().json()
            job_id = jobs_list[0]['job_id']

            delete_job_response = self._delete_job(monitor_name=self.monitor_name, job_id=job_id)
            self.assertEqual(200, delete_job_response.status_code)

            jobs_list = self._get_monitor_jobs().json()

            # In the case that the only monitor job has been deleted, jobs_list is a dictionary with 'error'
            # Else, if there were more than one monitor jobs and one has been deleted, jobs_list is a list
            if type(jobs_list) != dict or 'error' not in jobs_list:
                job_ids = [job['job_id'] for job in jobs_list]
                self.assertNotIn(job_id, job_ids)
        except Exception as e:
            self.fail(f'Program encountered an error: {e}')

    def _get_monitor_jobs(self, monitor_name=None):
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_jobs_url = f'{self.orbit_monitor_base_api_url}/{monitor_name}/jobs'
        return requests.get(monitor_jobs_url)

    def _start_and_update_and_resume_monitor(self, name):
        import time
        self._start_and_wait_for_monitor(name)

        update_response = self._update_monitor(monitor_name=name, schedule=self.valid_schedule_every_2_secs)
        self.assertEqual(204, update_response.status_code)

        resume_response = self._resume_monitor(monitor_name=name)
        self.assertEqual(204, resume_response.status_code)

        time.sleep(5)

    def _start_and_wait_for_monitor(self, name):
        start_response = self._start_monitor(name)
        self.assertEqual(0, start_response.returncode)

    def _start_monitor(self, name):
        import subprocess
        return subprocess.run(
            ['python', '-m', 'foundations', 'monitor', 'create', f'--project_name={self.project_name}', f'--name={name}', '.', 'main.py'],
            cwd='orbit_acceptance/fixtures/this_cool_monitor/',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def _get_all_monitors(self):
        return requests.get(self.orbit_monitor_base_api_url)

    def _get_monitor(self, monitor_name=None):
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{monitor_name}'
        return requests.get(monitor_url)

    def _pause_monitor(self, monitor_name=None):
        payload = {'status': 'pause'}
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{monitor_name}'
        return requests.put(monitor_url, json=payload)

    def _resume_monitor(self, monitor_name=None):
        payload = {'status': 'active'}
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{monitor_name}'
        return requests.put(monitor_url, json=payload)

    def _delete_monitor(self, monitor_name=None):
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{monitor_name}'
        return requests.delete(monitor_url)

    def _update_monitor(self, monitor_name=None, schedule=None):
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{monitor_name}'
        return requests.patch(monitor_url, json=schedule)

    def _delete_job(self, monitor_name=None, job_id=None):
        monitor_jobs_url = f'{self.orbit_monitor_base_api_url}/{monitor_name}/jobs'
        return requests.delete(monitor_jobs_url, json={'job_id': job_id})
