"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import os
import typing

import foundations
from foundations_spec import Spec, let, set_up
from foundations_rest_api.global_state import app_manager


class TestTensorboardEndpoint(Spec):
    url = '/api/v2beta/upload_to_tensorboard'
    client = app_manager.app().test_client()

    @set_up
    def set_up(self):
        from acceptance.cleanup import cleanup
        cleanup()

    @let
    def deployment(self) -> foundations.DeploymentWrapper:
        return foundations.deploy(
            project_name='test', 
            env='local', 
            entrypoint='tensorboard_job', 
            job_directory='acceptance/v2beta/fixtures/tensorboard_job', 
            params=None
        )

    @let
    def job_id(self) -> let:
        return self.deployment.job_name()

    @let
    def sync_directory(self) -> str:
        archives = os.environ['ARCHIVE_ROOT']
        return f'{archives}/sync'

    def test_upload_to_tensorflow(self):
        data = self.client.post(self.url, json={'job_ids': [self.job_id]})
        self.assertEqual(data.get_json(), f'Success! the specified jobs: [{self.job_id}] have been sent to tensorboard')

if __name__ == '__main__':
    def show_let(instance: object, let: let) -> None:
        print(let.evaluate(instance))

    test = TestTensorboardEndpoint()
    show_let(test, test.deployment)

