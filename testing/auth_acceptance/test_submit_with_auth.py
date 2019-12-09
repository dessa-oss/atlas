"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 12 2019
"""


from foundations_spec import *

class TestSubmitWithAuth(Spec):

    def test_submit_through_cli_fails_if_not_authenticated(self):
        import subprocess

        result = subprocess.run('foundations submit scheduler auth_acceptance/fixtures foundations_job.py',\
             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
        self.assertEqual(result.stdout.decode().strip(), 'Error running command: Not Authorized')