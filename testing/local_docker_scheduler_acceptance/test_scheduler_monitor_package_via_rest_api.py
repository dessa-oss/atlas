"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import requests

@quarantine
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
    def invalid_monitor_name(self):
        return self._gen_unique_word()

    @let
    def project_name(self):
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
        return f'http://localhost:5000/api/v1/projects/{self.project_name}/monitors'
    
    def test_pause_scheduled_monitor_package_via_api(self):
        self._start_and_wait_for_monitor()

        pause_response = self._pause_monitor()
        self.assertEqual(204, pause_response.status_code)

    def test_pause_scheduled_monitor_package_via_api_halts_execution_but_can_resume_later(self):
        self._start_and_wait_for_monitor()
        pause_response = self._pause_monitor()

        resume_response = self._resume_monitor()
        self.assertEqual(204, pause_response.status_code)

    def test_attempting_to_pause_invalid_monitor_should_produce_404(self):
        self._start_and_wait_for_monitor()

        pause_response = self._pause_monitor(monitor_name=self.invalid_monitor_name)
        self.assertEqual(404, pause_response.status_code)

    def test_attempting_to_resume_invalid_monitor_should_produce_404(self):
        self._start_and_wait_for_monitor()

        resume_response = self._resume_monitor(monitor_name=self.invalid_monitor_name)
        self.assertEqual(404, resume_response.status_code)
    
    def _start_and_wait_for_monitor(self):
        start_response = self._start_monitor()
        self.assertEqual(201, start_response.status_code)
    
    def _start_monitor(self):
        payload = {
            'name': self.monitor_name,
            'commands': self.commands,
            'job_directory': self.job_directory_binary
        }

        return requests.post(self.orbit_monitor_base_api_url, json=payload)

    def _get_all_monitors(self):
        return requests.get(self.orbit_monitor_base_api_url)

    def _get_monitors(self, monitor_name=None):
        monitor_name = monitor_name if self.monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{monitor_name}'
        return requests.get(monitor_url)

    def _pause_monitor(self, monitor_name=None):
        payload = {'status': 'pause'}
        monitor_name = monitor_name if self.monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{self.monitor_name}'
        return requests.put(monitor_url, json=payload)

    def _resume_monitor(self, monitor_name=None):
        payload = {'status': 'resume'}
        monitor_name = monitor_name if self.monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{self.monitor_name}'
        return requests.put(monitor_url, json=payload)

    def _delete_monitor(self, monitor_name=None):
        monitor_name = monitor_name if self.monitor_name is None else monitor_name
        monitor_url = f'{self.orbit_monitor_base_api_url}/{self.monitor_name}'
        return requests.delete(monitor_url, json=payload)