"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class FoundationsModelServer(object):

    def _create_pid_file(self):
        import os

        with open('/tmp/foundations_model_server.pid', 'w') as pidfile:
            pidfile.write(str(os.getpid()))

    def run(self):
        from flask import Flask

        self._create_pid_file()
        app = Flask(__name__)
        app.run()


if __name__ == '__main__':
    foundations_model_server = FoundationsModelServer()
    foundations_model_server.run()
