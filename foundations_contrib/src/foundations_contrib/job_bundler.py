"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.working_directory_stack import WorkingDirectoryStack


class JobBundler(object):

    def __init__(self, job_name, config, job, job_source_bundle):
        import os

        self._config = config
        self._config['job_name'] = job_name

        self._job_name = job_name
        self._job = job
        self._job_source_bundle = job_source_bundle

    def job_name(self):
        return self._job_name

    def bundle(self):
        self._job_source_bundle.bundle()
        self._save_job()
        self._save_config()
        self._bundle_job()
        self._job_source_bundle.cleanup()

    def unbundle(self):
        import tarfile

        with tarfile.open(self.job_archive(), 'r:gz') as tar:
            tar.extractall()

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

        with WorkingDirectoryStack():
            with tarfile.open(self.job_archive(), "w:gz") as tar:
                self._add_files_to_tarball(tar)

    def _add_files_to_tarball(self, tar):
        self._tar_job_source_bundle_archive(tar)
        self._tar_job_binary(tar)
        self._tar_config_files(tar)
        self._tar_foundations_modules(tar)
        if 'run_script_environment' in self._config or self._redis_password_set():
            self._tar_env(tar)
        self._tar_resources(tar)
    
    def _redis_password_set(self):
        import os
        return 'FOUNDATIONS_REDIS_PASSWORD' in os.environ

    def _tar_job_source_bundle_archive(self, tarfile):
        import os

        tarfile.add(self._job_source_bundle.job_archive(), arcname=os.path.join(self._job_name, 'job.tgz'))
    
    def _tar_job_binary(self, tarfile):
        import os

        tarfile.add(self._job_binary(), arcname=os.path.join(self._job_name, self._job_binary()))
    
    def _tar_config_files(self, tarfile):
        import glob
        import os

        for config_file in glob.glob('*.config.yaml'):
            tarfile.add(config_file, arcname=os.path.join(self._job_name, config_file))

    def _tar_env(self, tarfile):
        import os
        from foundations_contrib.simple_tempfile import SimpleTempfile
        from foundations_contrib.job_bundling.script_environment import ScriptEnvironment

        with SimpleTempfile('w+') as temp_file:
            ScriptEnvironment(self._config).write_environment(temp_file)
            tarfile.add(temp_file.name, arcname=os.path.join(self._job_name, 'run.env'))

    def _tar_resources(self, tarfile): 
        import os
        from foundations_contrib.resources_obfuscation_controller import ResourcesObfuscationController

        with ResourcesObfuscationController(self._config) as resources_obfuscation_controller:
            resources_directory = resources_obfuscation_controller.get_resources()
            os.chdir(resources_directory)
            tarfile.add(".", arcname=self._job_name)

    def _tar_foundations_modules(self, tarfile):
        import os
        from foundations_contrib.module_obfuscation_controller import ModuleObfuscationController

        with ModuleObfuscationController(self._config) as module_obfuscation_controller:
            for module_name, module_directory in module_obfuscation_controller.get_foundations_modules():
                self._log().debug('Adding module {} at {}'.format(module_name, module_directory))
                tarfile.add(module_directory, arcname=self._job_name + '/' + module_name)

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)
