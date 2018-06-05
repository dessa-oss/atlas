from vcat import *
from vcat_ssh import *

config_manager.config()['remote_user'] = 'thomas'
config_manager.config()['remote_host'] = 'localhost'
config_manager.config()['shell_command'] = '/bin/bash'
config_manager.config()[
    'code_path'] = '/home/thomas/Dev/Spiking/vcat-results/tmp/code'
config_manager.config()[
    'result_path'] = '/home/thomas/Dev/Spiking/vcat-results/tmp/results'
config_manager.config()['key_path'] = '/home/thomas/.ssh/id_local'
config_manager.config()['log_level'] = 'DEBUG'


class SpikePipelineArchive(object):

    def __init__(self, open_for_reading=False):
        self._archives = {}
        self._open_for_reading = open_for_reading

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        for archive in self._archives.values():
            archive.__exit__(exception_type, exception_value, traceback)
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
            archive = LocalBundledPipelineArchive(
                '/home/thomas/Dev/Spiking/vcat-results/tmp/results/' + name + '.tgz',
                self._open_for_reading
            )
            archive.__enter__()
            self._archives[name] = archive

        return self._archives[name]


archive_listing = SSHListing()

with SpikePipelineArchive(True) as bundled_archive:
    fetch = PipelineArchiverFetch(archive_listing, bundled_archive, bundled_archive,
                                  bundled_archive, bundled_archive, bundled_archive, bundled_archive)
    reader = ResultReader(fetch)
    print(reader.get_job_information())
