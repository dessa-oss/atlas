

from foundations_spec import *


class RunLocalJob(object):

    @let
    def job_id(self):
        return self.faker.uuid4()

    def _deploy_job_file(self, path, job_id=None, entrypoint='main.py'):
        from foundations_spec.extensions import run_process

        if job_id is None:
            job_id = self.job_id

        self._set_home_directory()
        return run_process(['python', entrypoint], path, environment={'FOUNDATIONS_HOME': self.foundations_home, 'FOUNDATIONS_JOB_ID': job_id, 'FOUNDATIONS_COMMAND_LINE': 'False'})

    def _run_job_file(self, path, job_id=None, entrypoint='main.py'):
        return self._deploy_job_file(path, job_id, entrypoint)

    def _set_home_directory(self):
        import os
        working_directory = os.getcwd()
        self.foundations_home = f'{working_directory}/foundations_home'

    def _update_environment_with_home_directory(self):
        import os
        self._set_home_directory()

        environment = {'FOUNDATIONS_HOME': self.foundations_home, 'FOUNDATIONS_COMMAND_LINE': 'False'}
        env = dict(os.environ)
        env.update(environment)
        return env