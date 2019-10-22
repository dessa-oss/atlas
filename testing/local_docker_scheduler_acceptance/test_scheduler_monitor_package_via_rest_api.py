"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import requests


class TestSchedulerMonitorPackageViaRESTAPI(Spec):

    sleep_time = 1
    existing_words = []

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
    def valid_schedule_1(self):
        return {'schedule': {
            'second': '*/5'}
        }

    @let
    def invalid_schedule_1(self):
        return {'schedule': {
            'days': '*',
            'seconds': '*/5'}
        }

    @let
    def invalid_schedule_2(self):
        return {'schedule': {
            'second': 'not-a-second'}
        }
    
    @skip('not implemented')
    def test_pause_scheduled_monitor_package_via_api(self):
        self._start_and_wait_for_monitor()

        pause_response = self._pause_monitor()
        self.assertEqual(204, pause_response.status_code)

    @skip('not implemented')
    def test_pause_scheduled_monitor_package_via_api_halts_execution_but_can_resume_later(self):
        self._start_and_wait_for_monitor()
        pause_response = self._pause_monitor()

        resume_response = self._resume_monitor()
        self.assertEqual(204, pause_response.status_code)

    @skip('not implemented')
    def test_attempting_to_pause_invalid_monitor_should_produce_404(self):
        self._start_and_wait_for_monitor()

        pause_response = self._pause_monitor(monitor_name=self.invalid_monitor_name)
        self.assertEqual(404, pause_response.status_code)

    @skip('not implemented')
    def test_attempting_to_resume_invalid_monitor_should_produce_404(self):
        self._start_and_wait_for_monitor()

        resume_response = self._resume_monitor(monitor_name=self.invalid_monitor_name)
        self.assertEqual(404, resume_response.status_code)

    def test_get_scheduled_monitors_returns_scheduled_monitors(self):
        import time

        self._start_and_wait_for_monitor(self.monitor_name)
        self._start_and_wait_for_monitor(self.monitor_name_2)

        monitors_response = self._get_all_monitors()
        monitors = monitors_response.json()
        self.assertIn(f'{self.project_name}-{self.monitor_name}', monitors)
        self.assertIn(f'{self.project_name}-{self.monitor_name_2}', monitors)

        monitor_package1 = f'{self.project_name}-{self.monitor_name}'
        monitor_package2 = f'{self.project_name}-{self.monitor_name_2}'

        delete_response1 = self._delete_monitor(self.monitor_name)
        self.assertEqual(204, delete_response1.status_code)

        delete_response2 = self._delete_monitor(self.monitor_name_2)
        self.assertEqual(204, delete_response2.status_code)

    def test_get_scheduled_monitor_returns_scheduled_monitor(self):
        self._start_and_wait_for_monitor(self.monitor_name)

        monitor_response = self._get_monitors(self.monitor_name)
        self.assertEqual(200, monitor_response.status_code)
        monitor_content = monitor_response.json()[f'{self.project_name}-{self.monitor_name}']

        expected_schedule = {
            'day': '*',
            'day_of_week': '*',
            'hour': '*',
            'minute': '*',
            'month': '*',
            'second': '*',
            'week': '*',
            'year': '*'
        }

        self.assertEqual(200, monitor_response.status_code)
        self.assertEqual('paused', monitor_content['status'])
        self.assertEqual(expected_schedule, monitor_content['schedule'])
        self.assertIsNone(monitor_content['next_run_time'])

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
        valid_schedule = self.valid_schedule_1
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

        delete_response = self._delete_monitor(self.monitor_name)
        self.assertEqual(204, delete_response.status_code)

    def test_update_schedule_on_monitor_with_correct_schedule_returns_204(self):
        import time
        self._start_and_wait_for_monitor(self.monitor_name)

        monitor_response = self._get_all_monitors()
        monitor_package = f'{self.project_name}-{self.monitor_name}'
        self.assertIn(monitor_package, monitor_response.json())

        valid_schedule = self.valid_schedule_1
        update_response = self._update_monitor(self.monitor_name, valid_schedule)
        self.assertEqual(204, update_response.status_code)
        time.sleep(5)
        delete_response = self._delete_monitor(self.monitor_name)
        self.assertEqual(204, delete_response.status_code)

    def _start_and_wait_for_monitor(self, name):
        start_response = self._start_monitor(name)
        self.assertEqual(0, start_response.returncode)

    def _start_monitor(self, name):
        import subprocess
        return subprocess.run(['python', '-m', 'foundations', 'monitor', 'start', f'--project_name={self.project_name}', f'--name={name}', '.', 'main.py'], cwd='local_docker_scheduler_acceptance/fixtures/this_cool_monitor/')

    def _get_all_monitors(self):
        return requests.get(self.orbit_monitor_base_api_url)

    def _get_monitors(self, monitor_name=None):
        monitor_name = monitor_name if self.monitor_name is None else self.monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{monitor_name}'
        return requests.get(monitor_url)

    def _pause_monitor(self, monitor_name=None):
        payload = {'status': 'pause'}
        monitor_name = monitor_name if self.monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{self.monitor_name}'
        return requests.put(monitor_url, json=payload)

    def _resume_monitor(self, monitor_name=None):
        payload = {'status': 'resume'}
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
