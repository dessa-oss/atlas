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

        sys.path.insert(0, job_root)
        os.chdir(job_root)

        manifest = self._job.manifest()
        module = manifest['entrypoints']['predict']['module']

        if '.' in module:
            top_level = module.split('.')[0]
            sys.path.insert(0, f'{job_root}/{top_level}')