"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class FoundationsModelServer(object):

    pid_file_path = '/var/tmp/foundations_model_server.pid'

    def run(self):
        try:
            self._create_new_pid_file()
            self._start_rest_api_server()
        except OSError as exception:
            self._log_server_failure(exception)

    def _start_rest_api_server(self):
        from foundations_production.serving.rest_api_server import RestAPIServer

        rest_api_server = RestAPIServer()
        rest_api_server.run()

    def _create_new_pid_file(self):
        import os

        self._remove_old_pid_file()
        self._create_pid_file()
        if not os.path.exists(self.pid_file_path):
            raise FileNotFoundError('Failed to create PID file for Foundations model server')

    def _remove_old_pid_file(self):
        import os

        try:
            os.remove(self.pid_file_path)
        except FileNotFoundError:
            pass

    def _create_pid_file(self):
        import os

        with open(self.pid_file_path, 'w') as pidfile:
            pidfile.write(str(os.getpid()))

    def _log_server_failure(self, exception):
        import logging
        
        logger = logging.getLogger()
        logger.error(str(exception))


if __name__ == '__main__':
    foundations_model_server = FoundationsModelServer()
    foundations_model_server.run()
