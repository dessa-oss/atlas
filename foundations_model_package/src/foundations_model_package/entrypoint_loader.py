"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class EntrypointLoader(object):
    
    def __init__(self, job):
        self._job = job

    def entrypoint_function(self, entrypoint_name):
        self._change_to_job_root_dir()
        self._add_module_to_sys_path(entrypoint_name)
        return self._load_function_from_module(entrypoint_name)

    def _module_name(self, entrypoint_name):
        return self._endpoint_information(entrypoint_name)['module']

    def _function_name(self, entrypoint_name):
        return self._endpoint_information(entrypoint_name)['function']

    def _load_function_from_module(self, entrypoint_name):
        from foundations_model_package.importlib_wrapper import load_function_from_module

        module_name = self._module_name(entrypoint_name)
        function_name = self._function_name(entrypoint_name)
        return load_function_from_module(module_name, function_name)

    def _add_module_to_sys_path(self, entrypoint_name):
        import os.path as path

        module_name = self._module_name(entrypoint_name)

        module_path = module_name.replace('.', '/')
        module_directory = path.dirname(module_path)

        if module_directory:
            self._add_to_sys_path(f'{self._job_root()}/{module_directory}')

    def _add_to_sys_path(self, directory):
        import sys
        sys.path.insert(0, directory)

    def _change_to_job_root_dir(self):
        import os

        self._check_job_root_dir_exists()

        self._add_to_sys_path(self._job_root())
        os.chdir(self._job_root())

    def _check_job_root_dir_exists(self):
        import os.path as path

        if not path.exists(self._job_root()):
            raise Exception(f'Job {self._job.id()} not found!')

    def _job_root(self):
        return self._job.root()

    def _endpoint_information(self, entrypoint_name):
        manifest = self._job.manifest()
        return manifest['entrypoints'][entrypoint_name]