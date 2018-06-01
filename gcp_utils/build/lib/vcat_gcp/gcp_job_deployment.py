from vcat.job_bundler import JobBundler


class GCPJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._config = {}

        self._gcp_bucket_connection = Client()
        self._code_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-code-test')
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')

        self._job_name = job_name
        self._job = job
        self._job_bundler = JobBundler(self._job_name, self._config, self._job, job_source_bundle)
        self._job_result_object = self._result_bucket_connection.blob(
            self._job_archive_name())

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
        return self._job_result_object.exists()

    def fetch_job_results(self):
        import os
        import tarfile
        import pickle

        if self._job_results is None:
            with open(self._job_results_archive(), 'w+b') as file:
                self._job_result_object.download_to_file(file)

            result = None
            with tarfile.open(self._job_results_archive(), "r:gz") as tar:
                for tarinfo in tar:
                    if os.path.splitext(tarinfo.name)[1] == ".pkl":
                        file = tar.extractfile(tarinfo)
                        result = pickle.load(file)
                        file.close()

            self._remove_job_results_archive()
            self._job_results = result

        return self._job_results

    def _run(self):
        job_object = self._code_bucket_connection.blob(
            self._job_archive_name())
        with open(self._job_archive(), 'rb') as file:
            job_object.upload_from_file(file)

    def _job_archive_name(self):
        return self._job_bundler.job_archive_name()

    def _job_archive(self):
        return self._job_bundler.job_archive()

    def _job_results_archive(self):
        return self._job_name + ".results.tgz"

    def _remove_job_results_archive(self):
        import os
        os.remove(self._job_results_archive())
