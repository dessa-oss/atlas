"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest
from mock import patch, Mock

from foundations.local_shell_job_deployment import LocalShellJobDeployment
from foundations.scheduler_local_backend import LocalBackend
from contextlib import contextmanager

class MockJobBundler(object):
    
    def __init__(self, job_name, config, job, job_source_bundle):
        pass

    def bundle(self):
        pass

    def unbundle(self):
        pass

    def cleanup(self):
        pass

    def job_archive(self):
        return 'dummy.tgz'

@contextmanager
def do_nothing(*args, **kwargs):
    yield

@patch('foundations.job_bundler.JobBundler', MockJobBundler)
@patch('shutil.rmtree', Mock(return_value='OK'))
@patch('foundations.change_directory.ChangeDirectory', do_nothing)
class TestLocalShellJobDeployment(unittest.TestCase):

    class MockBundle(object):

        def bundle(self):
            pass

        def job_archive(self):
            return 'dummy.tgz'

    def test_backend_returns_local_backend(self):
        self.assertEqual(LocalShellJobDeployment.scheduler_backend(), LocalBackend)

    @patch('subprocess.call')
    def test_deploy_executes_script_with_corret_parameters(self, mock):
        deployment = self._create_deployment()
        deployment.deploy()
        mock.assert_called_with(['/bin/bash', '-c', './run.sh'])

    @patch('subprocess.call')
    def test_deploy_executes_script_with_corret_parameters_different_shell_command(self, mock):
        deployment = self._create_deployment()
        deployment.config().update({'shell_command': 'C:\\Program Files\\Git\\bin\\bash.exe'})
        deployment.deploy()
        mock.assert_called_with(['C:\\Program Files\\Git\\bin\\bash.exe', '-c', './run.sh'])

    def _create_deployment(self):
        from foundations.job import Job
        from foundations import create_stage

        @create_stage
        def callback():
            pass

        job = Job(callback())
        bundle = self.MockBundle()
        return LocalShellJobDeployment('hello world', job, bundle)
