"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ScriptEnvironment(object):

    def __init__(self, config):
        self._config = config

    def write_environment(self, file):
        from pipes import quote
        import os
        if self._redis_password_is_set():
            file.write('export FOUNDATIONS_REDIS_PASSWORD={}\n'.format(self._redis_password()))

        for name, value in self._run_script_environment().items():
            file.write('export {}={}\n'.format(quote(name), quote(str(value))))
        file.flush()
        file.seek(0)

    def _run_script_environment(self):
        return self._config.get('run_script_environment', {})

    def _enable_stages(self):
        run_script_environment = self._run_script_environment()
        return run_script_environment.get('enable_stages', False)

    def _redis_password_is_set(self):
        return self._redis_password() is not None

    def _redis_password(self):
        import os
        return os.environ.get('FOUNDATIONS_REDIS_PASSWORD')