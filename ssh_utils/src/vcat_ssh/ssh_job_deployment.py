from vcat.job_bundler import JobBundler
from vcat_ssh.ssh_utils import SSHUtils


class SSHJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle):
        self._config = {}
        self._job_name = job_name
        self._job = job
        self._job_bundler = JobBundler(
            self._job_name, self._config, self._job, job_source_bundle)
        self._ssh_utils = SSHUtils(self._config)

    def config(self):
        return self._config

    def job_name(self):
        return self._job_name

    def deploy(self):
        self._job_bundler.bundle()
        try:
            self._deploy_internal()
        finally:
            self._job_bundler.cleanup()

    def is_job_complete(self):
        from subprocess import call

        command = self._check_job_done_ssh_command()
        return call(command) == 0

    def fetch_job_results(self):
        from subprocess import call
        from os.path import basename
        import dill as pickle
        import tarfile

        command = self._retrieve_scp_command()
        call(command)
        result = None
        with tarfile.open(self._results_archive_path(), 'r:gz') as tar:
            for tarinfo in tar:
                if basename(tarinfo.name) == "results.pkl":
                    file = tar.extractfile(tarinfo)
                    result = pickle.load(file)
                    file.close()

        return result

    def _deploy_internal(self):
        from subprocess import call

        command = self._deploy_scp_command()
        call(command)

    def _retrieve_scp_command(self):
        ssh_command = 'scp ' + self._ssh_utils.ssh_arguments() + ' ' + self._ssh_utils.user_at_host() + ':' + self._results_remote_archive_path() + ' ' + \
            self._results_archive_path()
        return self._ssh_utils.command_in_shell_command(ssh_command)

    def _deploy_scp_command(self):
        ssh_command = 'scp ' + self._ssh_utils.ssh_arguments() + ' ' + self._full_archive_path() + ' ' + \
            self._ssh_utils.user_at_host() + ':' + self._code_path()
        return self._ssh_utils.command_in_shell_command(ssh_command)

    def _check_job_done_ssh_command(self):
        ssh_command = 'ssh ' + self._ssh_utils.ssh_arguments() + ' ' + self._ssh_utils.user_at_host() + ' "stat ' + \
            self._result_path() + '/' + self._job_bundler.job_archive_name() + '"'
        return self._ssh_utils.command_in_shell_command(ssh_command)

    def _results_remote_archive_path(self):
        return self._result_path() + '/' + self._job_bundler.job_archive_name()

    def _results_archive_path(self):
        from os.path import abspath
        return abspath('../' + self._job_name + '.results.tgz')

    def _full_archive_path(self):
        from os.path import abspath
        return abspath(self._job_bundler.job_archive())

    def _code_path(self):
        return self._config['code_path']

    def _result_path(self):
        return self._config['result_path']
