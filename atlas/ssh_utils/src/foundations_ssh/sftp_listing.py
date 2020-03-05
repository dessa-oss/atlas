

class SFTPListing(object):

    def __init__(self, path_filter='*.tgz'):
        from foundations.global_state import config_manager
        from foundations_ssh.sftp_bucket import SFTPBucket

        self._config = config_manager.config()
        self._path_filter = path_filter
        self._bucket = SFTPBucket(self._result_path())

    def track_pipeline(self, pipeline_name):
        pass

    def get_pipeline_names(self):
        from foundations.utils import tgz_archive_without_extension

        archives = self._list_archive_names()
        return [tgz_archive_without_extension(archive_name) for archive_name in archives]

    def _list_archive_names(self):
        return self._bucket.list_files(self._path_filter)

    def _result_path(self):
        return self._config['result_path']