"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class FoundationsModelServer(object):

    pid_file_path = '/var/tmp/foundations_model_server.pid'

    def run(self, host='localhost', port=5000):
        try:
            self._create_new_pid_file()
            self._start_rest_api_server(host=host, port=port)
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


def _get_arguments():
    from argparse import ArgumentParser

    argument_parser = ArgumentParser(description='starts foundations model server')
    argument_parser.add_argument('--domain', type=str, help='domain and port used by foundations model server')
    return argument_parser.parse_args()


def _parse_domain(domain_string):
    if domain_string:
        host, port = domain_string.split(':')
        port = int(port)
    else:
        host = 'localhost'
        port = 5000
    return host, port


def main():
    parsed_arguments = _get_arguments()
    host, port = _parse_domain(parsed_arguments.domain)
    foundations_model_server = FoundationsModelServer()
    foundations_model_server.run(host=host, port=port)

if __name__ == '__main__':
    main()
