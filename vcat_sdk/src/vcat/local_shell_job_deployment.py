from vcat.job_bundler import JobBundler


class LocalShellJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle):
        self._config = {}
        self._job_name = job_name
        self._job = job
        self._job_bundler = JobBundler(self._job_name, self._config, self._job, job_source_bundle)
        self._results = {}

    def config(self):
        return self._config

    def job_name(self):
        return self._job_name

    def deploy(self):
        self._job_bundler.bundle()
        try:
            self._run()
        finally:
            pass
            # self._job_bundler.cleanup()

    def is_job_complete(self):
        return True

    def fetch_job_results(self):
        return self._results

    def _run(self):
        import shutil
        import subprocess
        import glob
        import dill as pickle
        script = "tar -xvf " + self._job_bundler.job_archive() + " && " + \
            "cd " + self._job_name + " && " + \
            "sh ./run.sh"
        args = ['/usr/bin/env', 'sh', '-c', script]
        subprocess.call(args)

        file_name = glob.glob(self._job_name + '/*.pkl')[0]
        with open(file_name, 'rb') as file:
            self._results = pickle.load(file)

        shutil.rmtree(self._job_name)
