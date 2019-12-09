"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""
import subprocess
import requests
import os
import time

from foundations_spec import *

class TestAuthViaClient(Spec):

    max_time_out_in_sec = 60

    @staticmethod
    def resolve_f9s_auth():
        import os.path as path
        return path.realpath('../foundations_contrib/src/')
        
    def start_and_wait_for_keycloak(self, klass):
        full_path = os.path.join(klass.resolve_f9s_auth(), "foundations_contrib/authentication")

        subprocess.run(
            ['bash', 'launch.sh'],
            cwd=full_path, 
            stdout=subprocess.PIPE)
        
        start_time = time.time()
        while time.time() - start_time < klass.max_time_out_in_sec:
            try:
                res = requests.get('http://localhost:8080/auth/')
                if res.status_code == 200:
                    return
            except Exception as e:
                time.sleep(1)
        self.fail('auth server never started')

    def test_cli_login(self):
        with self.assert_does_not_raise():
            subprocess.run('foundations login http://localhost:5558 -u test -p test', shell=True, check=True)
