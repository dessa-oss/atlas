class MultiSSHBundledPipelineArchive(object):

    def __init__(self):
        from vcat_ssh.ssh_utils import SSHUtils
        from vcat.global_state import config_manager

        self._archives = {}
        self._config = config_manager.config()
        self._ssh_utils = SSHUtils(self._config)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        from os import remove

        for name, archive in self._archives.items():
            archive.__exit__(exception_type, exception_value, traceback)
            remove(self._results_archive_path(name))
        self._archives = {}

    def append(self, name, item, prefix=None):
        return self._fetch_archive(prefix).append(name, item, self._modified_prefix(prefix))

    def append_binary(self, name, serialized_item, prefix=None):
        return self._fetch_archive(prefix).append_binary(name, serialized_item, self._modified_prefix(prefix))

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        return self._fetch_archive(prefix).append_file(file_prefix, file_path, self._modified_prefix(prefix), target_name)

    def fetch(self, name, prefix=None):
        return self._fetch_archive(prefix).fetch(name, self._modified_prefix(prefix))

    def fetch_binary(self, name, prefix=None):
        return self._fetch_archive(prefix).fetch_binary(name, self._modified_prefix(prefix))

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        return self._fetch_archive(prefix).fetch_to_file(file_prefix, file_path, self._modified_prefix(prefix), target_name)

    def _modified_prefix(self, prefix):
        return prefix + '/' + prefix

    def _fetch_archive(self, name):
        from vcat.local_bundled_pipeline_archive import LocalBundledPipelineArchive

        if name is None:
            raise StandardError('Cannot have a missing archive name')

        if not name in self._archives:
            self._retrieve_results(name)
            archive = LocalBundledPipelineArchive(
                self._results_archive_path(name),
                True
            )
            archive.__enter__()
            self._archives[name] = archive

        return self._archives[name]

    def _retrieve_results(self, name):
        from subprocess import call

        command = self._retrieve_scp_command(name)
        call(command)

    def _retrieve_scp_command(self, name):
        ssh_command = 'scp ' + self._ssh_utils.ssh_arguments() + ' ' + self._ssh_utils.user_at_host() + ':' + self._results_remote_archive_path(name) + ' ' + \
            self._results_archive_path(name)
        return self._ssh_utils.command_in_shell_command(ssh_command)

    def _results_archive_path(self, name):
        return '/tmp/' + name + '.tgz'

    def _results_remote_archive_path(self, name):
        return self._result_path() + '/' + name + '.tgz'

    def _result_path(self):
        return self._config['result_path']
