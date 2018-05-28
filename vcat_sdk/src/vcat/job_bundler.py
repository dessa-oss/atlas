class JobBundler(object):

    def __init__(self, job_name, config, job):
        import os

        self._config = config
        self._config['job_name'] = job_name

        self._job_name = job_name
        self._job = job
        self._module_directory = os.path.dirname(os.path.abspath(__file__))
        self._resource_directory = self._module_directory + "/resources"

    def job_name(self):
        return self._job_name

    def bundle(self):
        self._save_job()
        self._save_config()
        self._bundle_job()

    def cleanup(self):
        import os
        os.remove(self.job_archive())
        os.remove(self._job_binary())
        os.remove(self._job_config_yaml())

    def job_archive_name(self):
        return self._job_name + ".tgz"

    def job_archive(self):
        return "../" + self.job_archive_name()

    def _job_binary(self):
        return self._job_name + ".bin"

    def _job_results_archive(self):
        return self._job_name + ".results.tgz"

    def _job_config_yaml(self):
        return self._job_name + ".config.yaml"

    def _save_job(self):
        with open(self._job_binary(), "w+b") as file:
            file.write(self._job.serialize())

    def _save_config(self):
        import yaml
        with open(self._job_config_yaml(), 'w+') as file:
            yaml.dump(self._config, file)

    def _bundle_job(self):
        import tarfile
        import glob
        import os

        current_directory = os.getcwd()
        # os.chdir(self._module_directory)

        with tarfile.open(self.job_archive(), "w:gz") as tar:
            tar.add(".", arcname=self._job_name)

            os.chdir(self._module_directory)
            tar.add(".", arcname=self._job_name + "/vcat")

            os.chdir(self._resource_directory)
            tar.add(".", arcname=self._job_name)

        os.chdir(current_directory)
