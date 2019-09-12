"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import os
import typing

import foundations
from foundations_spec import *

class TestTensorboardEndpoint(Spec):
    url = '/api/v2beta/upload_to_tensorboard'

    @let
    def app_manager(self):
        from foundations_rest_api.global_state import app_manager
        return app_manager

    @let
    def client(self):
        return self.app_manager.app().test_client()

    @let
    def scheduler_host(self):
        from foundations_contrib.global_state import config_manager
        return config_manager['remote_host']

    @let
    def redis_url(self):
        from foundations_contrib.global_state import config_manager
        return config_manager['redis_url']
    
    @let
    def deployment(self) -> foundations.DeploymentWrapper:
        return foundations.submit(
            project_name='test', 
            entrypoint='tensorboard_job', 
            job_dir='scheduler_acceptance/fixtures/tensorboard_job'
        )

    @let
    def job_id(self) -> let:
        return self.deployment.job_name()

    @let
    def sync_directory(self) -> str:
        archives = os.environ['ARCHIVE_ROOT']
        return f'{archives}/sync'

    @set_up
    def set_up(self):
        import yaml
        from scheduler_acceptance.cleanup import cleanup
        cleanup()

        self.deployment.wait_for_deployment_to_complete()

    def test_upload_to_tensorflow(self):
        from foundations_contrib.global_state import config_manager

        data = self.client.post(self.url, json={'tensorboard_locations': [{'job_id': self.job_id, 'synced_directory': 'tb_data'}]})
        url = data.get_json()['url']
        self.assertEqual(f'{config_manager["TENSORBOARD_HOST"]}', url)

