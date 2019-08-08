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
        import sys
        import os
        import os.path as path

        job_root = self._job.root()

        if not path.exists(job_root):
            raise Exception(f'Job {self._job.id()} not found!')

        self._add_to_sys_path(job_root)
        os.chdir(job_root)

        module = self._module()

        module_path = module.replace('.', '/')
        module_directory = path.dirname(module_path)

        if module_directory:
            self._add_to_sys_path(f'{job_root}/{module_directory}')

    def _module(self):
        manifest = self._job.manifest()
        module = manifest['entrypoints']['predict']['module']

        return module

    def _add_to_sys_path(self, directory):
        import sys
        sys.path.insert(0, directory)