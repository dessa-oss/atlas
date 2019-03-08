"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest
import foundations
import foundations_contrib
import foundations_ssh
import subprocess

from mock import patch, Mock

from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
import test.ssh_utils_fixtures.sftp_job_deployment_fixtures as sjf
import foundations.constants as constants
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import *

class TestSFTPJobDeployment(Spec):

    mock_bytes_io = let_patch_mock('io.BytesIO')

    @let_now
    def mock_popen(self):
        mock = self.patch('subprocess.Popen')
        mock.return_value = self.mock_popen_instance
        return mock

    mock_popen_instance = let_mock()

    @let
    def process_output(self):
        return self.faker.sentence()

    @let
    def encoded_process_output(self):
        return self.process_output.encode('utf-8')

    @set_up
    def set_up(self):
        self.mock_popen_instance.communicate.return_value = [self.encoded_process_output]

    def test_scheduler_backend(self):
        from foundations_ssh.default_legacy_backend import default_legacy_backend
        self.assertEqual(SFTPJobDeployment.scheduler_backend(), default_legacy_backend)
    
    def test_job_queued(self):
        queued = sjf.QueuedMockDeployment()

        self.assertEqual(constants.deployment_queued, queued.get_job_status())

    def test_job_never_finishes(self):
        never_done = sjf.NeverFinishDeployment()

        self.assertEqual(constants.deployment_running, never_done.get_job_status())
        
    def test_job_completed_instantly(self):
        done = sjf.SuccessfulMockDeployment()

        self.assertEqual(constants.deployment_completed, done.get_job_status())

    def test_job_failed_instantly(self):
        failed = sjf.FailedMockDeployment()

        self.assertEqual(constants.deployment_error, failed.get_job_status())

    def test_takes_one_second(self):
        deploy = sjf.TakesOneSecond()

        for _ in range(0, 1):
            self.assertEqual(constants.deployment_running, deploy.get_job_status())

        self.assertEqual(constants.deployment_completed, deploy.get_job_status())
        self.assertEqual(constants.deployment_completed, deploy.get_job_status())

    def test_takes_two_seconds(self):
        deploy = sjf.TakesTwoSeconds()

        for _ in range(0, 2):
            self.assertEqual(constants.deployment_running, deploy.get_job_status())

        self.assertEqual(constants.deployment_completed, deploy.get_job_status())
        self.assertEqual(constants.deployment_completed, deploy.get_job_status())

    def test_takes_random_time(self):
        deploy = sjf.SuccessfulTakesRandomTime()

        while deploy.get_job_status() == constants.deployment_running:
            pass

        self.assertEqual(constants.deployment_completed, deploy.get_job_status())
        self.assertEqual(constants.deployment_completed, deploy.get_job_status())

    def test_fails_random_time(self):
        deploy = sjf.FailedTakesRandomTime()

        while deploy.get_job_status() == constants.deployment_running:
            pass

        self.assertEqual(constants.deployment_error, deploy.get_job_status())
        self.assertEqual(constants.deployment_error, deploy.get_job_status())
    
    @patch('foundations_ssh.sftp_bucket.SFTPBucket')
    @patch('foundations.global_state.config_manager')
    def test_get_job_logs_calls_popen_with_correct_arguments_to_ssh_into_scheduler(self, mock_config_manager, mock_sftp_bucket):
        config  = {
            'key_path': 'path/to/key.pem',
            'remote_host': '0.0.0.0',
            'code_path': '/home/foundations/jobs',
            'result_path': 'path/to/results'
        }

        mock_config_manager.config.return_value = config
        mock_config_manager.__getitem__ = lambda obj, key: config[key]

        sftp_job_deployment = SFTPJobDeployment('job_uuid', Mock(), Mock())
        sftp_job_deployment.get_job_logs()

        expected_args = ['ssh', '-i', 'path/to/key.pem', 'foundations@0.0.0.0', "'cat /home/foundations/logs/*/job_uuid.stdout'"]
        self.mock_popen.assert_called_with(expected_args, stdout=-1)
    
    @patch.object(subprocess.Popen, 'communicate')
    @patch('foundations_ssh.sftp_bucket.SFTPBucket')
    @patch('foundations.global_state.config_manager')
    def test_get_job_logs_returns_byte_io_as_string(self, mock_config_manager, mock_sftp_bucket, mock_communicate):
        config  = {
            'key_path': 'path/to/key.pem',
            'remote_host': '0.0.0.0',
            'code_path': '/home/foundations/jobs',
            'result_path': 'path/to/results'
        }

        mock_config_manager.config.return_value = config
        mock_config_manager.__getitem__ = lambda obj, key: config[key]

        sftp_job_deployment = SFTPJobDeployment('job_uuid', Mock(), Mock())
        self.assertEqual(sftp_job_deployment.get_job_logs(), self.process_output)
    
