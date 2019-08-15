"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

from mock import patch

from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
from foundations_contrib.scheduler_local_backend import LocalBackend
from foundations_spec import *
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


@patch('foundations_contrib.job_bundler.JobBundler', MockJobBundler)
@patch('shutil.rmtree', Mock(return_value='OK'))
@patch('foundations_contrib.change_directory.ChangeDirectory', do_nothing)
class TestLocalShellJobDeployment(Spec):

    @let_now
    def mock_os_environmet(self):
        return self.patch('os.environ', self.environment)

    @let
    def environment(self):
        environment = dict(self.environment_without_python_path)
        environment['PYTHONPATH'] = '/path/to/somewhere'
        return environment

    @let
    def environment_without_python_path(self):
        return self.faker.pydict()

    class MockBundle(object):

        def bundle(self):
            pass

        def job_archive(self):
            return 'dummy.tgz'

    def test_backend_returns_local_backend(self):
        self.assertEqual(
            LocalShellJobDeployment.scheduler_backend(), LocalBackend)

    @patch('subprocess.call')
    def test_deploy_executes_script_with_correct_parameters(self, mock):
        deployment = self._create_deployment()
        deployment.deploy()
        mock.assert_called_with(['/bin/bash', '-c', './run.sh'], env=self.environment_without_python_path)

    @patch('subprocess.call')
    def test_deploy_executes_script_with_correct_parameters_different_shell_command(self, mock):
        deployment = self._create_deployment()
        deployment.config().update(
            {'shell_command': 'C:\\Program Files\\Git\\bin\\bash.exe'})
        deployment.deploy()
        mock.assert_called_with(
            ['C:\\Program Files\\Git\\bin\\bash.exe', '-c', './run.sh'], env=self.environment_without_python_path)

    @patch('subprocess.call')
    def test_does_not_delete_python_path_if_does_not_exist(self, mock):
        self.environment.pop('PYTHONPATH')
        deployment = self._create_deployment()
        deployment.deploy()
        mock.assert_called_with(['/bin/bash', '-c', './run.sh'], env=self.environment_without_python_path)

    def _create_deployment(self):
        from foundations.job import Job
        from foundations import create_stage

        @create_stage
        def callback():
            pass

        job = Job(callback())
        bundle = self.MockBundle()
        return LocalShellJobDeployment('hello world', job, bundle)
