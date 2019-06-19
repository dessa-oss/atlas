"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestLocalDeployWithoutStages(Spec):

    @skip('Not implemented yet')
    def test_stageless_project_deploys_succesfully(self):
        import subprocess

        driver_deploy_exit_code = subprocess.call(["/bin/bash", "-c", "cd stageless_local_deployment/fixtures/stageless_project && python -m foundations deploy driver.py --env=local-stageless"])
        result_exit_code = subprocess.call(["/bin/bash", "-c", "cd stageless_local_deployment/fixtures/stageless_project && python -m foundations deploy results.py --env=local-stageless"])

        self.assertEqual(driver_deploy_exit_code, 0)
        self.assertEqual(result_exit_code, 0)
