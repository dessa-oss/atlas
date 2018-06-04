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
                    self._log.info('Running job %s', path)
                    self._log.info('Job %s is complete', path)

            sleep(0.5)
