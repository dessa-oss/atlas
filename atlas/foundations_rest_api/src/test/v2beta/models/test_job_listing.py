

from foundations_spec import *
from mock import patch
from foundations_rest_api.v2beta.models.job import Job
from foundations_core_rest_api_components.lazy_result import LazyResult

from foundations_rest_api.v2beta.models.job_artifact import JobArtifact

class TestJobListingV2(Spec):

    @let
    def fake_tags(self):
        return self.faker.pydict()

    @let
    def job_id(self):
        return self.faker.uuid4()

    mock_get_all_artifacts = let_patch_mock_with_conditional_return('foundations_rest_api.v2beta.models.job_artifact.JobArtifact.all')

    @set_up
    def set_up(self):
        import fakeredis
        from foundations_internal.foundations_context import FoundationsContext

        self._context = FoundationsContext()
        self.patch('foundations_rest_api.global_state.redis_connection', fakeredis.FakeRedis())

    def test_has_job_id(self):
        from uuid import uuid4

        job_id = str(uuid4())
        job = Job(job_id=job_id)

        self.assertEqual(job_id, job.job_id)

    def test_has_user(self):
        job = Job(user='Louis')
        self.assertEqual('Louis', job.user)

    def test_has_user_different_user(self):
        job = Job(user='Lenny')
        self.assertEqual('Lenny', job.user)

    def test_has_job_parameters(self):
        job = Job(job_parameters=['some list of parameters'])
        self.assertEqual(['some list of parameters'], job.job_parameters)

    def test_has_job_parameters_different_params(self):
        job = Job(job_parameters=['some different list of parameters'])
        self.assertEqual(
            ['some different list of parameters'], job.job_parameters)

    def test_has_output_metrics(self):
        job = Job(output_metrics={'a': 5})
        self.assertEqual({'a': 5}, job.output_metrics)

    def test_has_output_metrics_different_params(self):
        job = Job(output_metrics={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.output_metrics)

    def test_has_status_completed(self):
        job = Job(status='completed')
        self.assertEqual('completed', job.status)

    def test_has_status_running(self):
        job = Job(status='running')
        self.assertEqual('running', job.status)

    def test_has_status_different_params(self):
        job = Job(status='completed in error')
        self.assertEqual('completed in error', job.status)

    def test_has_start_time(self):
        job = Job(start_time=123423423434)
        self.assertEqual(123423423434, job.start_time)

    def test_has_start_time_different_params(self):
        job = Job(start_time=884234222323)
        self.assertEqual(884234222323, job.start_time)

    def test_has_completed_time(self):
        job = Job(completed_time=123423423434)
        self.assertEqual(123423423434, job.completed_time)

    def test_has_completed_time_none(self):
        job = Job(completed_time=None)
        self.assertIsNone(job.completed_time)

    def test_has_completed_time_different_params(self):
        job = Job(completed_time=884234222323)
        self.assertEqual(884234222323, job.completed_time)

    def test_job_has_tags(self):
        job = Job(tags=self.fake_tags)
        self.assertEqual(self.fake_tags, job.tags)

    def test_job_has_artifacts(self):
        artifact = JobArtifact(filename="output.txt", uri="output.txt", artifact_type='unknown')
        job = Job(artifacts=[artifact])
        self.assertEqual(artifact, job.artifacts[0])

    @patch('foundations_contrib.job_data_redis.JobDataRedis.get_all_jobs_data')
    def test_all_returns_multiple_jobs(self, mock_get_all_jobs_data):
        from test.datetime_faker import fake_current_datetime, restore_real_current_datetime

        fake_current_datetime(1005000000)

        self.mock_get_all_artifacts.return_when(LazyResult(lambda: []), job_id='my job x')
        self.mock_get_all_artifacts.return_when(LazyResult(lambda: []), job_id='00000000-0000-0000-0000-000000000007')

        mock_get_all_jobs_data.return_value = [
            {
                'project_name': 'random test project',
                'job_id': 'my job x',
                'user': 'some user',
                'job_parameters': {},
                'output_metrics': [],
                'status': 'completed',
                'start_time':  123456789,
                'completed_time': 2222222222,
                'tags': {},
                'artifacts': []
            },
            {
                'project_name': 'random test project',
                'job_id': '00000000-0000-0000-0000-000000000007',
                'user': 'soju hero',
                'job_parameters': {},
                'output_metrics': [],
                'status': 'running',
                'start_time': 999999999,
                'completed_time': None,
                'tags': {
                    'asdf': 'this',
                    'cool': 'dude'
                },
                'artifacts': []
            }
        ]

        expected_job_1 = Job(
            job_id='00000000-0000-0000-0000-000000000007',
            project='random test project',
            user='soju hero',
            job_parameters=[],
            output_metrics=[],
            status='running',
            start_time='2001-09-09T01:46:39',
            completed_time=None,
            duration='58d1h53m21s',
            tags={
                'asdf': 'this',
                'cool': 'dude'
            },
            artifacts=[]
        )

        expected_job_2 = Job(
            job_id='my job x',
            project='random test project',
            user='some user',
            job_parameters=[],
            output_metrics=[],
            status='completed',
            start_time='1973-11-29T21:33:09',
            completed_time='2040-06-02T03:57:02',
            duration='24291d6h23m53s',
            tags={},
            artifacts=[]
        )

        result = Job.all(project_name='random test project').evaluate()

        restore_real_current_datetime()

        expected_jobs = [expected_job_1, expected_job_2]
        self.assertEqual(expected_jobs, result)

    @patch('foundations_contrib.job_data_redis.JobDataRedis.get_all_jobs_data')
    def test_all_returns_multiple_jobs_with_artifacts(self, mock_get_all_jobs_data):
        from test.datetime_faker import fake_current_datetime, restore_real_current_datetime

        fake_current_datetime(1005000000)

        self.mock_get_all_artifacts.return_when(LazyResult(lambda: [
            JobArtifact(filename='output_x.png',uri='output_x.png', artifact_type='png')
        ]), job_id='my job x')

        self.mock_get_all_artifacts.return_when(LazyResult(lambda: [
            JobArtifact(filename='output_v007.wav', uri='output_v007.wav', artifact_type='wav'),
            JobArtifact(filename='output_v007.txt', uri='output_v007.txt', artifact_type='unknown'),
        ]), job_id='00000000-0000-0000-0000-000000000007')

        mock_get_all_jobs_data.return_value = [
            {
                'project_name': 'random test project',
                'job_id': 'my job x',
                'user': 'some user',
                'job_parameters': {},
                'output_metrics': [],
                'status': 'completed',
                'start_time':  123456789,
                'completed_time': 2222222222,
                'tags': {},
                'artifacts': [{'filename': 'output_x.png', 'uri': 'output_x.png', 'artifact_type': 'png'}]
            },
            {
                'project_name': 'random test project',
                'job_id': '00000000-0000-0000-0000-000000000007',
                'user': 'soju hero',
                'job_parameters': {},
                'output_metrics': [],
                'status': 'running',
                'start_time': 999999999,
                'completed_time': None,
                'tags': {
                    'asdf': 'this',
                    'cool': 'dude'
                },
                'artifacts': [
                    {'filename': 'output_v007.wav', 'uri': 'output_v007.wav', 'artifact_type': 'wav'},
                    {'filename': 'output_v007.txt', 'uri': 'output_v007.txt', 'artifact_type': 'unknown'},
                ]
            }
        ]

        expected_job_1 = Job(
            job_id='00000000-0000-0000-0000-000000000007',
            project='random test project',
            user='soju hero',
            output_metrics=[],
            job_parameters=[],
            status='running',
            start_time='2001-09-09T01:46:39',
            completed_time=None,
            duration='58d1h53m21s',
            tags={
                'asdf': 'this',
                'cool': 'dude'
            },
            artifacts=[
                JobArtifact(filename='output_v007.wav', uri='output_v007.wav', artifact_type='wav'),
                JobArtifact(filename='output_v007.txt', uri='output_v007.txt', artifact_type='unknown')
            ]
        )

        expected_job_2 = Job(
            job_id='my job x',
            project='random test project',
            user='some user',
            output_metrics=[],
            job_parameters=[],
            status='completed',
            start_time='1973-11-29T21:33:09',
            completed_time='2040-06-02T03:57:02',
            duration='24291d6h23m53s',
            tags={},
            artifacts=[JobArtifact(filename='output_x.png',uri='output_x.png', artifact_type='png')]
        )

        result = Job.all(project_name='random test project').evaluate()

        restore_real_current_datetime()

        expected_jobs = [expected_job_1, expected_job_2]
        self.assertEqual(expected_jobs, result)

    @patch('foundations_contrib.job_data_redis.JobDataRedis.get_all_jobs_data')
    def test_all_filters_out_non_hyperparameters(self, mock_get_all_jobs_data):
        from test.datetime_faker import fake_current_datetime, restore_real_current_datetime

        fake_current_datetime(1005000000)

        self.mock_get_all_artifacts.return_when(LazyResult(lambda: []), job_id='my job x')

        mock_get_all_jobs_data.return_value = [
            {
                'project_name': 'random test project',
                'job_id': 'my job x',
                'user': 'some user',
                'job_parameters': {'hello': 'world'},
                'output_metrics': [],
                'status': 'completed',
                'start_time':  123456789,
                'completed_time': 2222222222,
                'tags': {
                    'this': '1337'
                },
                'artifacts': []
            },
        ]

        expected_job_1 = Job(
            job_id='my job x',
            project='random test project',
            user='some user',
            output_metrics=[],
            job_parameters=[{'name': 'hello', 'value': 'world', 'type': 'string'}],
            status='completed',
            start_time='1973-11-29T21:33:09',
            completed_time='2040-06-02T03:57:02',
            duration='24291d6h23m53s',
            tags={
                'this': '1337'
            },
            artifacts=[]
        )

        result = Job.all(project_name='random test project').evaluate()

        restore_real_current_datetime()

        expected_jobs = [expected_job_1]
        self.assertEqual(expected_jobs, result)

    @patch('foundations_contrib.job_data_redis.JobDataRedis.get_all_jobs_data')
    def test_all_filters_out_non_hyperparameters_and_does_not_append_suffix_if_flag_false(self, mock_get_all_jobs_data):
        from test.datetime_faker import fake_current_datetime, restore_real_current_datetime

        fake_current_datetime(1005000000)

        self.mock_get_all_artifacts.return_when(LazyResult(lambda: []), job_id='my job x')

        mock_get_all_jobs_data.return_value = [
            {
                'project_name': 'random test project',
                'job_id': 'my job x',
                'user': 'some user',
                'job_parameters': {'hello': 'world'},
                'output_metrics': [],
                'status': 'completed',
                'start_time':  123456789,
                'completed_time': 2222222222,
                'tags': {
                    'beep': 'boop'
                },
                'artifacts': []
            },
        ]

        expected_job_1 = Job(
            job_id='my job x',
            project='random test project',
            user='some user',
            output_metrics=[],
            job_parameters=[{'name': 'hello', 'value': 'world', 'type': 'string'}],
            status='completed',
            start_time='1973-11-29T21:33:09',
            completed_time='2040-06-02T03:57:02',
            duration='24291d6h23m53s',
            tags={
                'beep': 'boop'
            },
            artifacts=[]
        )

        result = Job.all(project_name='random test project').evaluate()

        restore_real_current_datetime()

        expected_jobs = [expected_job_1]
        self.assertEqual(expected_jobs, result)

    def _make_job(self):
        from foundations_contrib.global_state import message_router
        from foundations_events.producers.jobs import QueueJob
        from foundations_events.producers.jobs import RunJob

        QueueJob(message_router, self._context).push_message()
        RunJob(message_router, self._context).push_message()

    def _assert_list_contains_items(self, expected, result):
        for item in expected:
            if not item in result:
                self.fail('Element {} not found in {}'.format(item, result))
