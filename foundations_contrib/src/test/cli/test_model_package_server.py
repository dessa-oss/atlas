"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.cli.model_package_server import *
import foundations_contrib

class TestModelPackageServer(Spec):
    
    mock_subprocess_run = let_patch_mock('subprocess.run')

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def model_name(self):
        return f'model-{self.faker.random.randint(1000, 9999)}'

    def test_deploy_runs_deployment_script_with_job_id(self):
        deploy(self.job_id)
        self.mock_subprocess_run.assert_called_with(['bash', './deploy_serving.sh', self.job_id], cwd=foundations_contrib.root() / 'resources/model_serving')

    def test_destroy_removes_deployment_with_model_name(self):
        destroy(self.model_name)
        self.mock_subprocess_run.assert_called_with(['bash', './remove_deployment.sh', self.model_name], cwd=foundations_contrib.root() / 'resources/model_serving')
