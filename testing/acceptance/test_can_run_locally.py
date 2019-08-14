"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.global_state import redis_connection


class TestCanRunLocally(Spec):

    @let
    def project_listing(self):
        from foundations_contrib.models.project_listing import ProjectListing

        return ProjectListing.list_projects(redis_connection)

    @let
    def project_names(self):
        return [project['name'] for project in self.project_listing]

    @let
    def project_name(self):
        return 'run_locally'

    @set_up
    def set_up(self):
        from acceptance.mixins.run_process import run_process

        self.job_id = run_process(['python', 'main.py'], 'acceptance/fixtures/run_locally').strip()

    def test_project_name_is_saved(self):
        self.assertIn('run_locally', self.project_names)

    def test_metrics_are_logged(self):
        from foundations_internal.fast_serializer import deserialize

        key = f'jobs:{self.job_id}:metrics'
        serialized_metric = redis_connection.lrange(key, 0, -1)[0]
        _, metric_key, metric_value = deserialize(serialized_metric)

        self.assertEqual('ugh', metric_key)
        self.assertEqual(10, metric_value)

    def test_artifacts_are_saved(self):
        import json

        serialized_artifact = redis_connection.get(f'jobs:{self.job_id}:user_artifact_metadata')
        artifact = json.loads(serialized_artifact)

        self.assertEqual('thomas_text.txt', artifact['key_mapping']['just_some_artifact'])

    def test_job_bundle_is_saved(self):
        import os.path

        path = os.path.expanduser('~/.foundations/job_data/archive')
        main_exists = os.path.exists(f'{path}/{self.job_id}/artifacts/main.py')
        self.assertTrue(main_exists)

        artifact_exists = os.path.exists(f'{path}/{self.job_id}/artifacts/thomas_text.txt')
        self.assertTrue(artifact_exists)

    def test_params_are_logged(self):
        import json

        key = f'jobs:{self.job_id}:parameters'
        serialized_metric = redis_connection.get(key)
        parameters = json.loads(serialized_metric)

        self.assertEqual(20, parameters['blah'])
