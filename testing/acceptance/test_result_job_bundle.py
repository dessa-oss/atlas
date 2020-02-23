

from foundations_spec import *
from contextlib import contextmanager
from acceptance.mixins.run_local_job import RunLocalJob

@quarantine
class TestResultJobBundle(Spec, RunLocalJob):

    @contextmanager
    def change_config(self):
        from foundations_contrib.config_manager import ConfigManager
        from foundations_contrib.global_state import config_manager

        config_manager.push_config()
        try:
            yield
        finally:
            config_manager.pop_config()
    
    @set_up
    def set_up(self):
        from acceptance.mixins.run_process import run_process
        from foundations_contrib.global_state import redis_connection
        import foundations

        self._deploy_job_file('acceptance/fixtures/run_locally')            
        self.local_job_id = redis_connection.get('foundations_testing_job_id').decode()
        
        with self.change_config():
            remote_job = foundations.submit(job_dir='acceptance/fixtures/run_locally', num_gpus=0)
        remote_job.wait_for_deployment_to_complete()
        self.remote_job_id = remote_job.job_name()

    @let
    def scheduler_config(self):
        from foundations_scheduler_plugin.config.scheduler import translate
        return translate({'results_config': {}, 'ssh_config': {}})

    @let
    def root_archive_directory(self):
        import os.path
        from foundations_contrib.utils import foundations_home

        return os.path.expanduser(foundations_home() + '/job_data/archive')

    @let
    def local_archive_directory(self):
        return f'{self.root_archive_directory}/{self.local_job_id}/artifacts/'

    @let
    def remote_archive_bucket(self):
        from foundations_contrib.global_state import config_manager
        from foundations_ssh.sftp_bucket import SFTPBucket

        config_manager.push_config()
        try:
            config_manager.config().update(self.scheduler_config)
            return SFTPBucket(f'/archive/archive/{self.remote_job_id}/artifacts/')
        finally:
            config_manager.pop_config()

    def test_local_run_job_bundle_is_same_as_remote(self):
        import os

        local_files = set(os.listdir(self.local_archive_directory))
        remote_files = set(self.remote_archive_bucket.list_files('*'))

        self.assertEqual(local_files, remote_files)