"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class SSHListing(object):

    def __init__(self, path_filter='*.tgz'):
        from vcat.global_state import config_manager
        from vcat_ssh.ssh_file_system_bucket import SSHFileSystemBucket

        self._config = config_manager.config()
        self._path_filter = path_filter
        self._bucket = SSHFileSystemBucket(self._result_path())

    def track_pipeline(self, pipeline_name):
        pass

    def get_pipeline_names(self):
        from vcat.utils import tgz_archive_without_extension

        archives = self._list_archive_names()
        return [tgz_archive_without_extension(archive_name) for archive_name in archives]

    def _list_archive_names(self):
        return self._bucket.list_files(self._path_filter)

    def _result_path(self):
        return self._config['result_path']
