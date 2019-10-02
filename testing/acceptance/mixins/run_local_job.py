"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *


class RunLocalJob(object):

    @let
    def job_id(self):
        return self.faker.uuid4()

    def _deploy_job_file(self, path, job_id=None, entrypoint='main.py'):
        from foundations_spec.extensions import run_process
        import os

        if job_id is None:
            job_id = self.job_id

        working_directory = os.getcwd()
        foundations_home = f'{working_directory}/foundations_home'
        return run_process(['python', entrypoint], path, environment={'FOUNDATIONS_HOME': foundations_home, 'FOUNDATIONS_JOB_ID': job_id, 'FOUNDATIONS_COMMAND_LINE': 'False'})

    def _run_job_file(self, path, job_id=None, entrypoint='main.py'):
        return self._deploy_job_file(path, job_id, entrypoint)
