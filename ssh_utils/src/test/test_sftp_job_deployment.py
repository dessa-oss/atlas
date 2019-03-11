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
from foundations_internal.testing.helpers.conditional_return import ConditionalReturn

class TestSFTPJobDeployment(Spec):

    mock_bytes_io = let_patch_mock('io.BytesIO')

    mock_datetime_class = let_mock()

    @let_now
    def mock_current_time(self):
        from datetime import datetime
        
        time = datetime(2019, 3, 11, 11, 10, 51, 546731)
        self.mock_datetime_class.now.return_value = time
        return time

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

    @let
    def remote_user(self):
        return self.faker.name()
    
    @let
    def fake_path(self):
        return self.faker.uri_path()
    
    @let 
    def job_name(self):
        return self.faker.sha1()

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
    def test_get_job_logs_creates_sftp_bucket_with_correct_path(self, mock_config_manager, mock_sftp_bucket):
        config  = {
            'code_path': self.fake_path + '/jobs',
            'result_path': 'path/to/results',
        }

        mock_config_manager.config.return_value = config
        mock_config_manager.__getitem__ = lambda obj, key: config[key]

        sftp_job_deployment = SFTPJobDeployment('job_uuid', Mock(), Mock())
        sftp_job_deployment.get_job_logs()
    
        mock_sftp_bucket.assert_called_with(self.fake_path + '/logs')
    
    @patch('foundations_ssh.sftp_bucket.SFTPBucket')
    @patch('foundations.global_state.config_manager')
    def test_get_job_logs_calls_sftp_download_as_string_with_correct_arguments(self, mock_config_manager, mock_sftp_bucket):
        config  = {
            'code_path': '/home/foundations/jobs',
            'result_path': 'path/to/results',
        }

        mock_config_manager.config.return_value = config
        mock_config_manager.__getitem__ = lambda obj, key: config[key]
    
        self.patch('datetime.datetime', self.mock_datetime_class)
        sftp_job_deployment = SFTPJobDeployment(self.job_name, Mock(), Mock())        
        
        mock_sftp_bucket_instance = Mock()
        mock_sftp_bucket.return_value = mock_sftp_bucket_instance
        mock_sftp_bucket_instance.download_as_string = ConditionalReturn()

        file_to_call = '2019-03-11/{}.stdout'.format(self.job_name)
        mock_sftp_bucket_instance.download_as_string.return_when(b'return_value', file_to_call)
        self.assertEqual(sftp_job_deployment.get_job_logs(), 'return_value')
    
