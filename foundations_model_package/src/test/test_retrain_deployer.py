"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import time

class TestRetrainDeployer(Spec):

    mock_orbit_deployer = let_patch_mock('foundations_contrib.cli.orbit_model_package_server.deploy')

    @let
    def project_name(self):
        return self.faker.word()
    
    @let
    def model_name(self):
        return self.faker.word()

    @let
    def project_directory(self):
        return self.faker.uri_path()

    @let
    def job_id(self):
        return self.faker.uuid4()
    @let
    def message(self):
        return {'job_id': self.job_id}

    # @skip('Not implemented')
    def test_calls_orbit_serve_start_with_correct_params(self):
        from foundations_model_package.retrain_deployer import RetrainDeployer
        
        retrain_deployer = RetrainDeployer(job_id=self.job_id, project_name=self.project_name, model_name=self.model_name, project_directory=self.project_directory)
        retrain_deployer.call(self.message, None, None)

        self.mock_orbit_deployer.assert_called_with(project_name=self.project_name, model_name=self.model_name, project_directory=self.project_directory, env='scheduler')

    def test_deploy_not_called_if_completed_job_id_does_not_match_retrain_deployer_job_id(self):
        from foundations_model_package.retrain_deployer import RetrainDeployer
        
        retrain_deployer = RetrainDeployer(job_id=self.job_id, project_name=self.project_name, model_name=self.model_name, project_directory=self.project_directory)
        retrain_deployer.call({'job_id': 'some_other_job_id'}, None, None)

        self.mock_orbit_deployer.assert_not_called()
