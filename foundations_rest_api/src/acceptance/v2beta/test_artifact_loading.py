"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2

class TestArtifactLoading(JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        from uuid import uuid4
        from copy import deepcopy
        import shutil
        
        import foundations
        import foundations_contrib.global_state as global_state
        from foundations_internal.foundations_context import FoundationsContext

        shutil.rmtree('/tmp/foundations_acceptance', ignore_errors=True)

        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name('hana')
        klass._some_artifacts = 'job_0'
        klass._no_artifacts = 'job_1'
        klass._one_artifact = 'job_2'

        klass._make_running_job(klass._one_artifact, 'soju hero', start_timestamp=99999999)
        klass._make_completed_job(klass._no_artifacts, 'beethoven', start_timestamp=100000000, end_timestamp=100086400)
        klass._make_completed_job(klass._some_artifacts, 'beethoven', start_timestamp=100000001, end_timestamp=100086400)

        klass._old_config = deepcopy(foundations.config_manager.config())
        klass._old_context = global_state.foundations_context

        foundations.config_manager.config().clear()
        foundations.config_manager.add_simple_config_path('acceptance/v2beta/fixtures/stageless_local.config.yaml')

        global_state.foundations_context = FoundationsContext(klass._pipeline)        

        klass._save_artifacts()

    @classmethod
    def tearDownClass(klass):
        import foundations
        import foundations_contrib.global_state as global_state
        from foundations_contrib.global_state import redis_connection as redis

        redis.flushall()

        foundations.config_manager.config().clear()
        foundations.config_manager.config().update(klass._old_config)

        global_state.foundations_context = klass._old_context

    @classmethod
    def _set_job_id(klass, job_id):
        import foundations_contrib.global_state as global_state

        context = global_state.foundations_context.pipeline_context()
        context.file_name = job_id

    @classmethod
    def _artifact_fixture_path(klass, artifact_name):
        import os.path as path
        return path.join('acceptance/v2beta/fixtures', artifact_name)

    @classmethod
    def _save_artifacts(klass):
        import foundations

        klass._set_job_id(klass._one_artifact)
        foundations.save_artifact(filepath=klass._artifact_fixture_path('image_file.png'))

        klass._set_job_id(klass._some_artifacts)
        foundations.save_artifact(filepath=klass._artifact_fixture_path('no_extension'))
        foundations.save_artifact(filepath=klass._artifact_fixture_path('other_file.other'))
        foundations.save_artifact(filepath=klass._artifact_fixture_path('audio_file.mp3'), key='audio_artifact')

    @skip('not implemented')
    def test_get_route(self):
        data = super().test_get_route()
        jobs = data['jobs']

        some_artifacts_payload = [
            {
                'filename': 'audio_artifact',
                'uri': f'api/v2beta/jobs/{self._some_artifacts}/artifacts/audio_artifact',
                'artifact_type': 'mp3'
            },
            {
                'filename': 'no_extension',
                'uri': f'api/v2beta/jobs/{self._some_artifacts}/artifacts/no_extension',
                'artifact_type': 'unknown'
            },
            {
                'filename': 'other_file.other',
                'uri': f'api/v2beta/jobs/{self._some_artifacts}/artifacts/other_file.other',
                'artifact_type': 'unknown'
            }
        ]

        self.assertEqual(some_artifacts_payload, jobs[0]['artifacts'])

        self.assertEqual([], jobs[1]['artifacts'])

        one_artifact_payload = [
            {
                'filename': 'image_file.png',
                'uri': f'api/v2beta/jobs/{self._one_artifact}/artifacts/image_file.png',
                'artifact_type': 'png'
            }
        ]

        self.assertEqual(one_artifact_payload, jobs[2]['artifacts'])