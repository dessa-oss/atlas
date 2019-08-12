"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.cli.orbit_model_package_server import deploy
from foundations_spec import *
import foundations_contrib


class TestOrbitModelPackageServer(Spec):
 
    mock_subprocess_run = let_patch_mock('subprocess.run')

    @let
    def mock_project_name(self):
        return self.faker.word()

    @let
    def mock_model_name(self):
        return self.faker.word()

    @let
    def mock_project_directory(self):
        return self.faker.uri_path()

    def test_deploy_run_deployment_script_with_project_name_model_name_project_directory(self):
        deploy(self.mock_project_name, self.mock_model_name, self.mock_project_directory)
        self.mock_subprocess_run.assert_called_with(['bash', './orbit/deploy_serving.sh', self.mock_project_name, self.mock_model_name, self.mock_project_directory], cwd=foundations_contrib.root() / 'resources/model_serving/orbit')

    def test_deploy_run_deployment_script_uploads_directory(self):
        pass

    