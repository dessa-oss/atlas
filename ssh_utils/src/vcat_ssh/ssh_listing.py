"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.utils import tgz_archive_without_extension
from vcat_ssh.ssh_utils import SSHUtils


class SSHListing(object):

    def __init__(self, path_filter='*.tgz'):
        from vcat.global_state import config_manager
        self._config = config_manager.config()
        self._ssh_utils = SSHUtils(self._config)
        self._path_filter = path_filter

    def track_pipeline(self, pipeline_name):
        pass

    def get_pipeline_names(self):
        archives = self._list_archive_names()
        return [tgz_archive_without_extension(archive_name) for archive_name in archives]

    def _list_archive_names(self):
        from os.path import basename

        archives = self._list_archives()
        return [basename(path) for path in archives]

    def _list_archives(self):
        from subprocess import Popen
        from subprocess import PIPE
        from vcat.utils import split_process_output

        command = self._list_archives_command()
        stdout, _, _ = self._ssh_utils.execute_command(command)
        return split_process_output(stdout)

    def _list_archives_command(self):
        return self._ssh_utils.command_in_ssh_command('ls -1 ' + self._result_path() + '/' + self._path_filter)

    def _result_path(self):
        return self._config['result_path']
