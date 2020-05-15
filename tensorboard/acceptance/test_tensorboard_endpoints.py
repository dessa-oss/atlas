import os

import foundations
from foundations_spec import *

from unittest import skip

@quarantine
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
    def deployment(self):
        return foundations.submit(
            project_name='tensorboard',
            entrypoint='tensorboard_job',
            job_dir='fixtures/tensorboard_job'
        )

    @let
    def job_id(self):
        return self.deployment.job_name()

    @let
    def sync_directory(self) -> str:
        archives = os.environ['ARCHIVE_ROOT']
        return f'{archives}/sync'

    @set_up
    def set_up(self):
        cleanup()

        self.deployment.wait_for_deployment_to_complete()

    def test_upload_to_tensorflow(self):
        from foundations_contrib.global_state import config_manager

        data = self.client.post(self.url, json={'job_ids': [self.job_id]})
        url = data.get_json()['url']
        self.assertEqual(f'{config_manager["TENSORBOARD_HOST"]}', url)

def cleanup():
    import shutil
    from os import getcwd, remove
    from os.path import isdir
    from glob import glob
    from foundations_contrib.global_state import redis_connection, foundations_job
    from foundations_internal.pipeline_context import PipelineContext
    from foundations_internal.pipeline import Pipeline

    tmp_dir = getcwd() + '/foundations_home/job_data'
    if isdir(tmp_dir):
        shutil.rmtree(tmp_dir)

    for file in glob('*.tgz'):
        remove(file)

    pipeline_context = PipelineContext()
    pipeline = Pipeline(pipeline_context)
    foundations_job._pipeline = pipeline
