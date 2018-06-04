from vcat.utils import tgz_archive_without_extension
from vcat.local_file_system_bucket import LocalFileSystemBucket


class SimpleWorker(object):

    def __init__(self, code_path, result_path):
        from logging import getLogger

        self._log = getLogger(__name__)
        self._code_path = code_path
        self._result_path = result_path
        self._code_bucket = LocalFileSystemBucket(self._code_path)

    def run(self):
        from time import sleep

        started_jobs = set()
        while True:
            for path in self._code_bucket.list_files('*.tgz'):
                if not path in started_jobs:
                    started_jobs.add(path)
                    self._run_job(path)

            sleep(0.5)

    def _run_job(self, archive_path):
        try:
            self._log.info('Running job %s', archive_path)
            self._extract_archive(archive_path)
            self._log.info('Job %s is complete', archive_path)

        finally:
            self._remove_job_directory(archive_path)

    def _remove_job_directory(self, archive_path):
        from shutil import rmtree
        from os.path import basename
        
        archive_name = basename(archive_path)
        job_path = tgz_archive_without_extension(archive_name)
        rmtree(job_path)

    def _extract_archive(self, archive_path):
        import tarfile

        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall()
