"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from acceptance.mixins.metrics_fetcher import MetricsFetcher

import foundations

@skip
class TestDeployJobViaDeployFunction(Spec, MetricsFetcher):
    
    @let
    def job_directory(self):
        return '/tmp/deploy_job_test'

    @let
    def project_directory(self):
        return 'acceptance/fixtures/deploy_job_via_function_project'

    @let
    def entrypoint(self):
        return 'entrypoint.py'

    @let
    def environment(self):
        return 'an_environment'

    @let
    def project_name(self):
        return 'this-project'

    @let
    def expected_metrics(self):
        return {
            'learning_rate': 0.125,
            'layer_0_neuron': 5,
            'layer_1_neuron': 6
        }

    def test_deploy_job_with_all_arguments_specified_deploys_job(self):
        import shutil

        shutil.rmtree(self.job_directory, ignore_errors=True)
        shutil.copytree(self.project_directory, self.job_directory)

        job_uuid = foundations.deploy(job_directory=self.job_directory, entrypoint=self.entrypoint, project_name=self.project_name, env=self.environment)
        
        for metric_name, expected_metric_value in self.expected_metrics.items():
            self.assertEqual(expected_metric_value, self._get_logged_metric(self.project_name, job_uuid, metric_name))