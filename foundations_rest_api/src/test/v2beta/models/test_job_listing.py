"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

from foundations_spec import *
from mock import patch
from foundations_rest_api.v2beta.models.job import Job


class TestJobListingV2(Spec):

    @let
    def fake_tags(self):
        return self.faker.pydict()

    @set_up
    def set_up(self):
        from foundations_internal.pipeline import Pipeline
        from foundations_internal.pipeline_context import PipelineContext
        from foundations_contrib.global_state import redis_connection

        redis_connection.flushall()

        self._pipeline_context = PipelineContext()
        self._pipeline = Pipeline(self._pipeline_context)

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

    def test_has_input_params(self):
        job = Job(input_params=['some list of parameters'])
        self.assertEqual(['some list of parameters'], job.input_params)

    def test_has_input_params_different_params(self):
        job = Job(input_params=['some different list of parameters'])
        self.assertEqual(
            ['some different list of parameters'], job.input_params)

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

    @patch('foundations_contrib.job_data_redis.JobDataRedis.get_all_jobs_data')
    def test_all_returns_multiple_jobs(self, mock_get_all_jobs_data):
        from test.datetime_faker import fake_current_datetime, restore_real_current_datetime

        fake_current_datetime(1005000000)

        mock_get_all_jobs_data.return_value = [
            {
                'project_name': 'random test project',
                'job_id': 'my job x',
                'user': 'some user',
                'job_parameters': {},
                'input_params': [],
                'output_metrics': [],
                'status': 'completed',
                'start_time':  123456789,
                'completed_time': 2222222222,
                'tags': {}
            },
            {
                'project_name': 'random test project',
                'job_id': '00000000-0000-0000-0000-000000000007',
                'user': 'soju hero',
                'job_parameters': {},
                'input_params': [],
                'output_metrics': [],
                'status': 'running',
                'start_time': 999999999,
                'completed_time': None,
                'tags': {
                    'asdf': 'this',
                    'cool': 'dude'
                }
            }
        ]

        expected_job_1 = Job(
            job_id='00000000-0000-0000-0000-000000000007',
            project='random test project',
            user='soju hero',
            input_params=[],
            output_metrics=[],
            status='running',
            start_time='2001-09-09T01:46:39',
            completed_time=None,
            duration='58d1h53m21s',
            tags={
                'asdf': 'this',
                'cool': 'dude'
            }
        )

        expected_job_2 = Job(
            job_id='my job x',
            project='random test project',
            user='some user',
            input_params=[],
            output_metrics=[],
            status='completed',
            start_time='1973-11-29T21:33:09',
            completed_time='2040-06-02T03:57:02',
            duration='24291d6h23m53s',
            tags={}
        )

        result = Job.all(project_name='random test project').evaluate()

        restore_real_current_datetime()

        expected_jobs = [expected_job_1, expected_job_2]
        self.assertEqual(expected_jobs, result)

    @patch('foundations_contrib.job_data_redis.JobDataRedis.get_all_jobs_data')
    def test_all_filters_out_non_hyperparameters(self, mock_get_all_jobs_data):
        from test.datetime_faker import fake_current_datetime, restore_real_current_datetime

        fake_current_datetime(1005000000)

        mock_get_all_jobs_data.return_value = [
            {
                'project_name': 'random test project',
                'job_id': 'my job x',
                'user': 'some user',
                'job_parameters': {'hello': 'world'},
                'input_params': [
                    {
                        'argument': {
                            'name': 'hello',
                            'value': {'name': 'hello', 'type': 'dynamic'}
                        },
                        'stage_uuid': '0'
                    },
                    {
                        'argument': {
                            'name': 'hello',
                            'value': {'value': '33', 'type': 'constant'}
                        },
                        'stage_uuid': '0'
                    },
                ],
                'output_metrics': [],
                'status': 'completed',
                'start_time':  123456789,
                'completed_time': 2222222222,
                'tags': {
                    'this': '1337'
                }
            },
        ]

        expected_job_1 = Job(
            job_id='my job x',
            project='random test project',
            user='some user',
            input_params=[
                {'name': 'hello-1', 'value': 'world', 'type': 'string', 'source': 'placeholder'}],
            output_metrics=[],
            status='completed',
            start_time='1973-11-29T21:33:09',
            completed_time='2040-06-02T03:57:02',
            duration='24291d6h23m53s',
            tags={
                'this': '1337'
            }
        )

        result = Job.all(project_name='random test project').evaluate()

        restore_real_current_datetime()

        expected_jobs = [expected_job_1]
        self.assertEqual(expected_jobs, result)

    @patch('foundations_contrib.job_data_redis.JobDataRedis.get_all_jobs_data')
    def test_all_filters_out_non_hyperparameters_and_does_not_append_suffix_if_flag_false(self, mock_get_all_jobs_data):
        from test.datetime_faker import fake_current_datetime, restore_real_current_datetime

        fake_current_datetime(1005000000)

        mock_get_all_jobs_data.return_value = [
            {
                'project_name': 'random test project',
                'job_id': 'my job x',
                'user': 'some user',
                'job_parameters': {'hello': 'world'},
                'input_params': [
                    {
                        'argument': {
                            'name': 'hello',
                            'value': {'name': 'hello', 'type': 'dynamic'}
                        },
                        'stage_uuid': '0'
                    },
                    {
                        'argument': {
                            'name': 'hello',
                            'value': {'value': '33', 'type': 'constant'}
                        },
                        'stage_uuid': '0'
                    },
                ],
                'output_metrics': [],
                'status': 'completed',
                'start_time':  123456789,
                'completed_time': 2222222222,
                'tags': {
                    'beep': 'boop'
                }
            },
        ]

        expected_job_1 = Job(
            job_id='my job x',
            project='random test project',
            user='some user',
            input_params=[
                {'name': 'hello', 'value': 'world', 'type': 'string', 'source': 'placeholder'}],
            output_metrics=[],
            status='completed',
            start_time='1973-11-29T21:33:09',
            completed_time='2040-06-02T03:57:02',
            duration='24291d6h23m53s',
            tags={
                'beep': 'boop'
            }
        )

        result = Job.all(project_name='random test project', handle_duplicate_param_names=False).evaluate()

        restore_real_current_datetime()

        expected_jobs = [expected_job_1]
        self.assertEqual(expected_jobs, result)

    def _make_stage(self, uuid, function, *args, **kwargs):
        from foundations_internal.stage_connector_wrapper_builder import StageConnectorWrapperBuilder

        builder = StageConnectorWrapperBuilder(self._pipeline_context)
        builder = builder.uuid(uuid)
        builder = builder.stage(self._pipeline.uuid(), function, args, kwargs)
        builder = builder.hierarchy([self._pipeline.uuid()])
        return builder.build()

    def _make_job(self):
        from foundations_contrib.global_state import message_router
        from foundations_contrib.producers.jobs.queue_job import QueueJob
        from foundations_contrib.producers.jobs.run_job import RunJob

        QueueJob(message_router, self._pipeline_context).push_message()
        RunJob(message_router, self._pipeline_context).push_message()

    def _assert_list_contains_items(self, expected, result):
        for item in expected:
            if not item in result:
                self.fail('Element {} not found in {}'.format(item, result))
