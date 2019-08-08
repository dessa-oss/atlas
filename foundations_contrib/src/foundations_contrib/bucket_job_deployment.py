"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class BucketJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle, code_bucket, results_bucket):
        from foundations.global_state import config_manager
        from foundations_contrib.job_bundler import JobBundler

        self._config = {}
        self._config.update(config_manager.config())
        self._config['_is_deployment'] = True

        self._code_bucket = code_bucket
        self._result_bucket = results_bucket

        self._job_name = job_name
        self._job = job
        self._job_bundler = JobBundler(
            self._job_name, self._config, self._job, job_source_bundle)

        self._job_results = None

    def config(self):
        return self._config

    def job_name(self):
        return self._job_name

    def deploy(self):
        self._job_bundler.bundle()
        try:
            self._run()
        finally:
            self._job_bundler.cleanup()

    def is_job_complete(self):
        return self._result_bucket.exists(self._job_archive_name())

    def fetch_job_results(self):
        import os
        import tarfile
        from foundations_internal.serializer import deserialize_from_file
        from foundations_contrib.simple_tempfile import SimpleTempfile

        if self._job_results is None:
            with SimpleTempfile('w+b') as temp_file:
                self._result_bucket.download_to_file(
                    self._job_archive_name(), temp_file)

                with tarfile.open(temp_file.name, "r:gz") as tar:
                    for tarinfo in tar:
                        if os.path.splitext(tarinfo.name)[1] == ".pkl":
                            file = tar.extractfile(tarinfo)
                            self._job_results = deserialize_from_file(file)
                            file.close()

        return self._job_results

    def _job_archive_name(self):
        return self._job_bundler.job_archive_name()

    def upload_to_result_bucket(self):
        self._bucket_upload_from_file(self._result_bucket)
        
    def _run(self):
        self._bucket_upload_from_file(self._code_bucket)

    def _bucket_upload_from_file(self, bucket):
        with open(self._job_archive(), 'rb') as file:
            bucket.upload_from_file(self._job_archive_name(), file)

    def _job_archive_name(self):
        return self._job_bundler.job_archive_name()

    def _job_archive(self):
        return self._job_bundler.job_archive()
