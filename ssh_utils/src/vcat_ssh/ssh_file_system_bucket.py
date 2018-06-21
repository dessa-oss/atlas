"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.simple_tempfile import SimpleTempfile


class SSHFileSystemBucket(object):

    def __init__(self, path):
        from vcat_ssh.ssh_utils import SSHUtils
        from vcat.global_state import config_manager

        self._path = path
        self._ssh_utils = SSHUtils(config_manager.config())

    def upload_from_string(self, name, data):
        with SimpleTempfile('w+b') as temp_file:
            temp_file.write_and_flush(data)
            self.upload_from_file(name, temp_file)

    def upload_from_file(self, name, input_file):
        self._ensure_path_exists(name)
        self._ssh_utils.execute_to_remote_scp(
            input_file.name, self._remote_path(name))

    def exists(self, name):
        from subprocess import call

        command = self._list_files_command(name)
        return self._ssh_utils.call_command(command) == 0

    def download_as_string(self, name):
        from vcat.utils import byte_string

        with SimpleTempfile('w+b') as temp_file:
            self.download_to_file(name, temp_file)
            data_bytes = temp_file.read()
            return byte_string(data_bytes)

    def download_to_file(self, name, output_file):
        self._ssh_utils.execute_to_local_scp(
            self._remote_path(name), output_file.name)

    def list_files(self, pathname):
        from os.path import basename

        file_paths = self._list_remote_files(pathname)
        return [basename(path) for path in file_paths]

    def _remote_path(self, name):
        return self._path + '/' + name

    def _list_remote_files(self, pathname):
        from vcat.utils import split_process_output

        command = self._list_files_command(pathname)
        listing, _, _ = self._ssh_utils.execute_command(command)
        return split_process_output(listing)

    def _list_files_command(self, pathname):
        shell_command = 'ls -1 ' + self._path + '/' + pathname
        return self._ssh_utils.command_in_ssh_command(shell_command)

    def _ensure_path_exists(self, name):
        command = self._ensure_path_exists_command(name)
        _, _, status_code = self._ssh_utils.execute_command(command)
        if status_code != 0:
            raise Exception('Unable to create directory for remote path {}'.format(
                self._remote_path(name)))

    def _ensure_path_exists_command(self, name):
        from os.path import dirname

        directory = dirname(self._remote_path(name))

        shell_command = 'mkdir -p ' + directory
        return self._ssh_utils.command_in_ssh_command(shell_command)
