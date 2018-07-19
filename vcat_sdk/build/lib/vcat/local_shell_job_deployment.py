"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.job_bundler import JobBundler


class LocalShellJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle):
        from vcat.global_state import config_manager
        self._config = {}
        self._config.update(config_manager.config())

        self._job_name = job_name
        self._job = job
        self._job_bundler = JobBundler(
            self._job_name, self._config, self._job, job_source_bundle)
        self._results = {}

    def config(self):
        return self._config

    def job_name(self):
        return self._job_name

    def deploy(self):
        self._job_bundler.bundle()
        try:
            self._run()
        finally:
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
        import shutil
        import subprocess
        import glob
        import tarfile
        from vcat.change_directory import ChangeDirectory
        from vcat.serializer import deserialize_from_file

        with tarfile.open(self._job_bundler.job_archive(), 'r:gz') as tar:
            tar.extractall()
            
        with ChangeDirectory(self._job_name):
            script = "{} ./run.sh".format(self._shell_command())
            args = self._command_in_shell_command(script)
            subprocess.call(args)

        file_name = glob.glob(self._job_name + '/*.pkl')[0]
        with open(file_name, 'rb') as file:
            self._results = deserialize_from_file(file)

        shutil.rmtree(self._job_name)

    def _command_in_shell_command(self, command):
        return [self._shell_command(), '-c', command]

    def _shell_command(self):
        return self._config.get('shell_command', '/bin/bash')
