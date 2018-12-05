"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class LocalShellJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle):
        from foundations.global_state import config_manager
        from foundations_contrib.job_bundler import JobBundler

        self._config = {}
        self._config.update(config_manager.config())

        self._job_name = job_name
        self._job = job
        self._job_bundler = JobBundler(
            self._job_name, self._config, self._job, job_source_bundle)
        self._results = {}

    @staticmethod
    def scheduler_backend():
        """Returns the local shell deployment scheduler backend implementation

        Returns:
            LegacyScheduler -- As above
        """

        from foundations_contrib.scheduler_local_backend import LocalBackend
        return LocalBackend

    def config(self):
        return self._config

    def job_name(self):
        return self._job_name

    def deploy(self):
        import shutil
        self._job_bundler.bundle()
        try:
            self._run()
        finally:
            shutil.rmtree(self._job_name)
            self._job_bundler.cleanup()

    def is_job_complete(self):
        return True

    def get_job_status(self):
        results = self.fetch_job_results()

        try:
            error_information = results["global_stage_context"]["error_information"]

            if error_information is not None:
                return "Error"
            else:
                return "Completed"
        except:
            return "Error"

    def fetch_job_results(self):
        return self._results

    def _run(self):
        import subprocess
        import glob
        from foundations_contrib.change_directory import ChangeDirectory
        from foundations_internal.serializer import deserialize_from_file

        self._job_bundler.unbundle()

        with ChangeDirectory(self._job_name):
            script = './run.sh'
            args = self._command_in_shell_command(script)
            subprocess.call(args)

        results = glob.glob(self._job_name + '/*.pkl')
        if results:
            file_name = results[0]
            with open(file_name, 'rb') as file:
                self._results = deserialize_from_file(file)

    def _command_in_shell_command(self, command):
        return [self._shell_command(), '-c', command]

    def _shell_command(self):
        return self._config.get('shell_command', '/bin/bash')
