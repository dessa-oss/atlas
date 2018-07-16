"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.utils import tgz_archive_without_extension
from vcat.local_file_system_bucket import LocalFileSystemBucket
from vcat.change_directory import ChangeDirectory


class SimpleBucketWorker(object):

    def __init__(self, code_bucket, result_bucket):
        self._code_bucket = code_bucket
        self._result_bucket = result_bucket

    def run(self):
        from time import sleep

        started_jobs = set()
        while True:
            self.run_once(started_jobs)
            sleep(0.5)

    def run_once(self, started_jobs):
        for archive_name in self._code_bucket.list_files('*.tgz'):
            if not archive_name in started_jobs:
                started_jobs.add(archive_name)
                self._handle_job(archive_name)

    def _handle_job(self, archive_name):
        self._log().info('Running job %s', archive_name)
        status_code = self._run_job(archive_name)
        if status_code == 0:
            self._log().info('Job %s is complete', archive_name)
        else:
            self._log().info('Job failed with status code %d', status_code)

    def _run_job(self, archive_name):
        try:
            self._extract_archive(archive_name)
            return self._execute_job(archive_name)
        finally:
            self._bundle_job_results(archive_name)
            self._remove_job_directory(archive_name)

    def _bundle_job_results(self, archive_name):
        import tarfile
        from vcat import SimpleTempfile

        job_name = self._job_name(archive_name)
        with SimpleTempfile('w+b') as temp_file:
            with tarfile.open(temp_file.name, 'w:gz') as tar:
                tar.add(job_name)
            self._result_bucket.upload_from_file(archive_name, temp_file.file)

    def _execute_job(self, archive_name):
        job_name = self._job_name(archive_name)
        with ChangeDirectory(job_name):
            return self._execute_job_command()

    def _execute_job_command(self):
        from subprocess import call
        return call(['/usr/bin/env', 'sh', '-c', './run.sh'])

    def _remove_job_directory(self, archive_name):
        from shutil import rmtree

        job_path = self._job_name(archive_name)
        rmtree(job_path)

    def _job_name(self, archive_name):
        return tgz_archive_without_extension(archive_name)

    def _extract_archive(self, archive_name):
        import tarfile
        from vcat import SimpleTempfile

        with SimpleTempfile('w+b') as temp_file:
            self._code_bucket.download_to_file(archive_name, temp_file.file)
            with tarfile.open(temp_file.name, 'r:gz') as tar:
                tar.extractall()

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
