"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class EntrypointLoader(object):
    
    def __init__(self, job):
        self._job = job

    def entrypoint_function(self):
        import os.path as path
        from foundations_model_package.importlib_wrapper import load_function_from_module

        self._change_to_job_root_dir()

        module_name = self._module_name()

        module_path = module_name.replace('.', '/')
        module_directory = path.dirname(module_path)

        if module_directory:
            self._add_to_sys_path(f'{self._job_root()}/{module_directory}')

        manifest = self._job.manifest()
        function_name = manifest['entrypoints']['predict']['function']

        function = load_function_from_module(module_name, function_name)

        return function

    def _module_name(self):
        manifest = self._job.manifest()
        module = manifest['entrypoints']['predict']['module']

        return module

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