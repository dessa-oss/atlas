"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class MultiSFTPBundledPipelineArchive(object):

    def __init__(self):
        from foundations.global_state import config_manager
        from foundations_ssh.sftp_bucket import SFTPBucket

        self._archives = {}
        self._config = config_manager.config()
        self._bucket = SFTPBucket(self._result_path())

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

    def fetch_file_path(self, file_prefix, file_path, prefix=None):
        return self._fetch_archive(prefix).fetch_file_path(file_prefix, file_path, self._modified_prefix(prefix))

    def fetch_file_path_to_target_file_path(self, file_prefix, file_path, prefix=None, target_name=None):
        return self._fetch_archive(prefix).fetch_file_path_to_target_file_path(file_prefix, file_path, self._modified_prefix(prefix), target_name)

    def _modified_prefix(self, prefix):
        return prefix + '/' + prefix

    def _fetch_archive(self, name):
        from foundations.local_bundled_pipeline_archive import LocalBundledPipelineArchive

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
        with open(target, 'w+b') as file:
            self._bucket.download_to_file(name + '.tgz', file)

    def _generate_results_archive_path(self):
        from tempfile import gettempdir
        from os.path import join
        from uuid import uuid4

        name = str(uuid4())
        return join(gettempdir(), name + '.tgz')

    def _result_path(self):
        return self._config['result_path']
