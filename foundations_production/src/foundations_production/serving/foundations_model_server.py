"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class FoundationsModelServer(object):

    pid_file_path = '/var/tmp/foundations_model_server.pid'

    def run(self):
        from flask import Flask

        self._create_pid_file()
        app = Flask(__name__)
        app.run()

    def _create_pid_file(self):
        import os

        with open(self.pid_file_path, 'w') as pidfile:
            pidfile.write(str(os.getpid()))

if __name__ == '__main__':
    foundations_model_server = FoundationsModelServer()
    foundations_model_server.run()
