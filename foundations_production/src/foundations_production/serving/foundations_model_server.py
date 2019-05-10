"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class FoundationsModelServer(object):

    pid_file_path = '/var/tmp/foundations_model_server.pid'

    def run(self, domain='localhost', port=5000):
        try:
            self._create_new_pid_file()
            self._start_rest_api_server(host=domain, port=port)
        except OSError as exception:
            self._log_server_failure(exception)

    def _start_rest_api_server(self, host='localhost', port=5000):
        from foundations_production.serving.rest_api_server import RestAPIServer

        rest_api_server = RestAPIServer()
        rest_api_server.run(host=host, port=port)

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

def main():
    from argparse import ArgumentParser

    argument_parser = ArgumentParser(help='starts foundations model server')
    argument_parser.add_argument('--domain', type=str, help='domain and port used by foundations model server')
    parsed_arguments = argument_parser.parse_args()
    if parsed_arguments.domain:
        domain, port = parsed_arguments.domain.split(':')
        port = int(port)
    else:
        domain = 'localhost'
        port = 5000
    foundations_model_server = FoundationsModelServer()
    foundations_model_server.run(domain=domain, port=port)

if __name__ == '__main__':
    main()
