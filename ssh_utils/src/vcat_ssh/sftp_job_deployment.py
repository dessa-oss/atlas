"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class SFTPJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle):
        from vcat.job_bundler import JobBundler
        from vcat.global_state import config_manager

        self._config = {}
        self._config.update(config_manager.config())

        self._job_name = job_name
        self._job = job
        self._job_bundler = JobBundler(
            self._job_name, self._config, self._job, job_source_bundle)
        self._code_bucket = None
        self._result_bucket = None

    def config(self):
        return self._config

    def job_name(self):
        return self._job_name

    def deploy(self):
        self._job_bundler.bundle()
        try:
            with open(self._job_bundler.job_archive(), 'rb') as file:
                self._get_code_bucket().upload_from_file(self._job_bundler.job_archive_name(), file)
        finally:
            self._job_bundler.cleanup()

    def is_job_complete(self):
        return self._get_result_bucket().exists(self._job_bundler.job_archive_name())

    def fetch_job_results(self):
        from os.path import basename
        import tarfile
        from vcat.simple_tempfile import SimpleTempfile
        from vcat.serializer import deserialize_from_file

        result = None
        with SimpleTempfile('w+b') as temp_file:
            self._get_result_bucket().download_to_file(
                self._job_bundler.job_archive_name(), temp_file)
            with tarfile.open(temp_file.name, 'r:gz') as tar:
                for tarinfo in tar:
                    if basename(tarinfo.name) == "results.pkl":
                        file = tar.extractfile(tarinfo)
                        result = deserialize_from_file(file)
                        file.close()

        return result

    def _get_code_bucket(self):
        from vcat_ssh.sftp_bucket import SFTPBucket

        if self._code_bucket is None:
            self._code_bucket = SFTPBucket(self._code_path())
        return self._code_bucket

    def _get_result_bucket(self):
        from vcat_ssh.sftp_bucket import SFTPBucket

        if self._result_bucket is None:
            self._result_bucket = SFTPBucket(self._result_path())
        return self._result_bucket

    def _code_path(self):
        return self._config['code_path']

    def _result_path(self):
        return self._config['result_path']
