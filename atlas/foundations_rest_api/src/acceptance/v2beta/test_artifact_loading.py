
from foundations_spec import *

from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2


class TestArtifactLoading(JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        from copy import deepcopy
        import shutil
        
        import foundations_contrib.global_state as global_state
        from foundations_internal.foundations_job import FoundationsJob

        shutil.rmtree('/tmp/foundations_acceptance', ignore_errors=True)

        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name(JobsTestsHelperMixinV2._str_random_uuid())
        klass._some_artifacts = JobsTestsHelperMixinV2._str_random_uuid()
        klass._no_artifacts = JobsTestsHelperMixinV2._str_random_uuid()
        klass._one_artifact = JobsTestsHelperMixinV2._str_random_uuid()

        random_uuid = JobsTestsHelperMixinV2._str_random_uuid()

        klass._make_running_job(klass._one_artifact, JobsTestsHelperMixinV2._str_random_uuid(), start_timestamp=99999999)
        klass._make_completed_job(klass._no_artifacts, random_uuid, start_timestamp=100000000, end_timestamp=100086400)
        klass._make_completed_job(klass._some_artifacts, random_uuid, start_timestamp=100000001, end_timestamp=100086400)

        klass._old_config = deepcopy(global_state.config_manager.config())
        klass._old_context = global_state.foundations_job

        global_state.config_manager.reset()

        global_state.foundations_job = FoundationsJob()

        klass._save_artifacts()

    @classmethod
    def tearDownClass(klass):
        import foundations_contrib.global_state as global_state

        global_state.config_manager.reset()
        global_state.config_manager.config().update(klass._old_config)

        global_state.foundations_job = klass._old_context

    @classmethod
    def _set_job_id(klass, job_id):
        import foundations_contrib.global_state as global_state

        job = global_state.foundations_job
        job.job_id = job_id

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

    def test_get_route(self):
        data = super().test_get_route()
        jobs = data['jobs']

        some_artifacts_payload = [
            {
                'filename': 'audio_file.mp3',
                'uri': f'https://archive.dessa.com/archive/{self._some_artifacts}/user_artifacts/audio_file.mp3',
                'artifact_type': 'audio',
                'archive_key': 'audio_artifact'
            },
            {
                'filename': 'no_extension',
                'uri': f'https://archive.dessa.com/archive/{self._some_artifacts}/user_artifacts/no_extension',
                'artifact_type': 'unknown',
                'archive_key': 'no_extension'
            },
            {
                'filename': 'other_file.other',
                'uri': f'https://archive.dessa.com/archive/{self._some_artifacts}/user_artifacts/other_file.other',
                'artifact_type': 'unknown',
                'archive_key': 'other_file.other'
            }
        ]

        self.assertEqual(some_artifacts_payload, jobs[0]['artifacts'])

        self.assertEqual([], jobs[1]['artifacts'])

        one_artifact_payload = [
            {
                'filename': 'image_file.png',
                'uri': f'https://archive.dessa.com/archive/{self._one_artifact}/user_artifacts/image_file.png',
                'artifact_type': 'image',
                'archive_key': 'image_file.png'
            }
        ]

        self.assertEqual(one_artifact_payload, jobs[2]['artifacts'])