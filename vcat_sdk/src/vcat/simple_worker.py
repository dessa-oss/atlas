"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.utils import tgz_archive_without_extension
from vcat.local_file_system_bucket import LocalFileSystemBucket
from vcat.change_directory import ChangeDirectory


class SimpleWorker(object):

    def __init__(self, code_path, result_path):
        self._code_path = code_path
        self._result_path = result_path
        self._code_bucket = LocalFileSystemBucket(self._code_path)

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
                archive_path = self._job_code_path(archive_name)
                self._handle_job(archive_path)

    def _job_code_path(self, archive_name):
        from os.path import join
        return join(self._code_path, archive_name)

    def _handle_job(self, archive_path):
        self._log().info('Running job %s', archive_path)
        status_code = self._run_job(archive_path)
        if status_code == 0:
            self._log().info('Job %s is complete', archive_path)
        else:
            self._log().info('Job failed with status code %d', status_code)

    def _run_job(self, archive_path):
        try:
            self._extract_archive(archive_path)
            return self._execute_job(archive_path)
        finally:
            self._bundle_job_results(archive_path)
            self._remove_job_directory(archive_path)
            self._remove_archive(archive_path)

    def _remove_archive(self, archive_path):
        from os import remove
        remove(archive_path)

    def _bundle_job_results(self, archive_path):
        import tarfile
        from shutil import move
        from vcat.utils import ensure_path_exists

        job_name = self._job_name(archive_path)
        with tarfile.open(self._source_job_results_archive(job_name), 'w:gz') as tar:
            tar.add(job_name)
        
        ensure_path_exists(self._result_path, job_name + '.tgz')
        move(self._source_job_results_archive(job_name), self._target_job_results_archive(job_name))

    def _source_job_results_archive(self, job_name):
        return job_name + '.results.tgz'

    def _target_job_results_archive(self, job_name):
        return self._result_path + '/' + job_name + '.tgz'

    def _execute_job(self, archive_path):
        job_name = self._job_name(archive_path)
        with ChangeDirectory(job_name):
            return self._execute_job_command()

    def _execute_job_command(self):
        from subprocess import call
        return call(['/usr/bin/env', 'sh', '-c', './run.sh'])

    def _remove_job_directory(self, archive_path):
        from shutil import rmtree

        job_path = self._job_name(archive_path)
        rmtree(job_path)

    def _job_name(self, archive_path):
        from os.path import basename

        archive_name = basename(archive_path)
        return tgz_archive_without_extension(archive_name)

    def _extract_archive(self, archive_path):
        import tarfile

        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall()

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
