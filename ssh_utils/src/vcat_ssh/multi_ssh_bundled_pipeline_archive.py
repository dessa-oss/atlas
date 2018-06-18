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
        for archive in self._archives.values():
            archive.__exit__(exception_type, exception_value, traceback)
            archive.remove_archive()
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
            raise Exception('Cannot have a missing archive name')

        if not name in self._archives:
            target = self._generate_results_archive_path()
            self._retrieve_results(name, target)
            archive = LocalBundledPipelineArchive(
                target,
                True
            )
            archive.__enter__()
            self._archives[name] = archive

        return self._archives[name]

    def _retrieve_results(self, name, target):
        command = self._retrieve_scp_command(name, target)
        self._ssh_utils.safe_execute_command(command)

    def _retrieve_scp_command(self, name, target):
        return self._ssh_utils.to_local_scp_command(self._results_remote_archive_path(name), target)

    def _generate_results_archive_path(self):
        from tempfile import gettempdir
        from os.path import join
        from uuid import uuid4

        name = str(uuid4())
        return join(gettempdir(), name + '.tgz')

    def _results_remote_archive_path(self, name):
        return self._result_path() + '/' + name + '.tgz'

    def _result_path(self):
        return self._config['result_path']
