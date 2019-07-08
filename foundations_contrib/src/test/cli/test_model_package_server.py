"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.cli.model_package_server import deploy
import foundations_contrib

class TestModelPackageServer(Spec):
    
    mock_subprocess_run = let_patch_mock('subprocess.run')

    @let
    def job_id(self):
        return self.faker.uuid4()

    def test_runs_deployment_script_with_job_id(self):
        deploy(self.job_id)
        self.mock_subprocess_run.assert_called_with(['bash', './deploy_serving.sh', self.job_id], cwd=foundations_contrib.root() / 'resources/model_serving')