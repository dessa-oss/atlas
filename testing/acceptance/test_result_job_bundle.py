"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from contextlib import contextmanager

class TestResultJobBundle(Spec):

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
                    
        run_process(['python', 'main.py'], 'acceptance/fixtures/run_locally')
        self.local_job_id = redis_connection.get('foundations_testing_job_id').decode()
        
        with self.change_config():
            self.remote_job_id = foundations.deploy(env='default', job_directory='acceptance/fixtures/run_locally').job_name()

    @let
    def root_archive_directory(self):
        import os.path
        from foundations_contrib.utils import foundations_home

        return os.path.expanduser(foundations_home() + '/job_data/archive')

    @let
    def local_archive_directory(self):
        return f'{self.root_archive_directory}/{self.local_job_id}/artifacts/'

    @let
    def remote_archive_directory(self):
        return f'{self.root_archive_directory}/{self.remote_job_id}/artifacts/'

    def test_local_run_job_bundle_is_same_as_remote(self):
        import os

        local_files = set(os.listdir(self.local_archive_directory))
        remote_files = set(os.listdir(self.remote_archive_directory))

        self.assertEqual(local_files, remote_files)