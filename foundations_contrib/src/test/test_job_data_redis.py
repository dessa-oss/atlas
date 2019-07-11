"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
import json
import pickle
import fakeredis
from mock import patch
import six

from foundations_spec import *
from foundations_contrib.job_data_redis import JobDataRedis
from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
from foundations.global_state import redis_connection


class TestJobDataRedis(Spec):

    def setUp(self):
        self._redis = fakeredis.FakeStrictRedis()
        self._redis.flushdb()

    def _set_redis(self, job_id, parameter, data):
        self._redis.set('jobs:{}:{}'.format(job_id, parameter), data)

    def _rpush_redis(self, job_id, parameter, data):
        self._redis.rpush('jobs:{}:{}'.format(job_id, parameter), data)

    def _hmset_redis(self, job_id, parameter, data):
        self._redis.hmset(f'jobs:{job_id}:{parameter}', data)

    def _load_data_new_job(self, job_id, data):
        set_parameter_name = ['project', 'start_time',
                              'completed_time', 'user', 'state', 'parameters', 'input_parameters']
        rpush_parameter_name = ['metrics']
        hmset_parameter_name = ['tags']

        for key, value in data.items():
            if key in set_parameter_name:
                self._set_redis(job_id, key, value)
            if key in rpush_parameter_name:
                self._rpush_redis(job_id, key, value)
            if key in hmset_parameter_name:
                for hm_key, hm_value in value.items():
                    self._hmset_redis(job_id, 'annotations', {hm_key: hm_value})

    def _sadd_redis_project_name(self, project_name, job_id):
        self._redis.sadd(
            'project:{}:jobs:running'.format(project_name), job_id)

    def test_get_job_data_gets_data(self):
        data = {
            'project': 'banana',
            'user': 'potter',
            'parameters': json.dumps({'harry': 'potter'}),
            'input_parameters': self._foundations_serialize([{'ron': 'weasley'}]),
            'metrics': self._fast_serialize(('123', 'hermione', 'granger')),
            'state': 'dead',
            'start_time': '456',
            'completed_time': '123',
            'tags': {}
        }
        job_id = 'the boy who lived'
        redis_pipe = RedisPipelineWrapper(
            self._redis.pipeline())
        job_data = JobDataRedis(redis_pipe, job_id)
        self._load_data_new_job(job_id, data)

        result = job_data.get_job_data(True)
        redis_pipe.execute()
        expected_result = {
            'project_name': 'banana',
            'job_id': job_id,
            'user': 'potter',
            'job_parameters': {'harry': 'potter'},
            'input_params': [{'ron': 'weasley'}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'dead',
            'start_time': float('456'),
            'completed_time': float('123'),
            'tags': {}
        }
        self.assertDictEqual(expected_result, result.get())

    def test_get_job_data_gets_data_skips_inputs(self):
        data = {
            'project': 'banana',
            'user': 'potter',
            'parameters': json.dumps({'harry': 'potter'}),
            'input_parameters': self._foundations_serialize([{'ron': 'weasley'}]),
            'metrics': self._fast_serialize(('123', 'hermione', 'granger')),
            'state': 'dead',
            'start_time': '456',
            'completed_time': '123',
            'tags': {
                'this_tag': 123,
                'that_tag': 'asdf'
            }
        }
        job_id = 'the boy who lived'
        redis_pipe = RedisPipelineWrapper(
            self._redis.pipeline())
        job_data = JobDataRedis(redis_pipe, job_id)
        self._load_data_new_job(job_id, data)

        result = job_data.get_job_data(False)
        redis_pipe.execute()
        expected_result = {
            'project_name': 'banana',
            'job_id': job_id,
            'user': 'potter',
            'job_parameters': {'harry': 'potter'},
            'input_params': [],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'dead',
            'start_time': float('456'),
            'completed_time': float('123'),
            'tags': {
                'this_tag': '123',
                'that_tag': 'asdf'
            }
        }
        self.assertDictEqual(expected_result, result.get())

    def test_get_job_data_gets_data_default_data(self):
        data = {}
        job_id = 'the boy who lived'
        redis_pipe = RedisPipelineWrapper(
            self._redis.pipeline())
        job_data = JobDataRedis(redis_pipe, job_id)
        self._load_data_new_job(job_id, data)

        result = job_data.get_job_data(True)
        redis_pipe.execute()
        expected_result = {
            'project_name': None,
            'job_id': job_id,
            'user': None,
            'job_parameters': {},
            'input_params': [],
            'output_metrics': [],
            'status': None,
            'start_time': None,
            'completed_time': None,
            'tags': {}
        }
        self.assertDictEqual(expected_result, result.get())

    def test_get_job_data_gets_data_different_data(self):
        data = {
            'project': 'apple',
            'user': 'potter',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': self._foundations_serialize([{'harry': 'weasley'}]),
            'metrics': self._fast_serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'tags': {
                'bep': 'bip'
            }
        }
        job_id = 'sushine'
        redis_pipe = RedisPipelineWrapper(
            self._redis.pipeline())
        job_data = JobDataRedis(redis_pipe, job_id)
        self._load_data_new_job(job_id, data)

        result = job_data.get_job_data(True)
        redis_pipe.execute()

        expected_result = {
            'project_name': 'apple',
            'job_id': job_id,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'harry': 'weasley'}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123'),
            'tags': {
                'bep': 'bip'
            }
        }

        self.assertDictEqual(expected_result, result.get())

    def test_get_job_data_all_jobs_single_job(self):
        project_name = 'apple'
        data = {
            'project': project_name,
            'user': 'potter',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': self._foundations_serialize([{'harry': 'weasley'}]),
            'metrics': self._fast_serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'tags': {
                'bep': 'bip'
            }
        }
        job_id_1 = 'sushine'

        self._sadd_redis_project_name(project_name, job_id_1)
        self._load_data_new_job(job_id_1, data)

        expected_result_1 = {
            'project_name': project_name,
            'job_id': job_id_1,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'harry': 'weasley'}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123'),
            'tags': {
                'bep': 'bip'
            }
        }

        results = JobDataRedis.get_all_jobs_data(
            project_name, self._redis, True)

        self.assertDictEqual(results[0], expected_result_1)

    def test_get_job_data_all_jobs_single_job_different_data(self):
        project_name = 'pomme'
        data = {
            'project': project_name,
            'user': 'baker',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': self._foundations_serialize([{'harry': 'weasley'}]),
            'metrics': self._fast_serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'tags': {
                'bep': 'bip'
            }
        }
        job_id_1 = 'sushine'

        self._sadd_redis_project_name(project_name, job_id_1)
        self._load_data_new_job(job_id_1, data)

        expected_result_1 = {
            'project_name': project_name,
            'job_id': job_id_1,
            'user': 'baker',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'harry': 'weasley'}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123'),
            'tags': {
                'bep': 'bip'
            }
        }

        results = JobDataRedis.get_all_jobs_data(
            project_name, self._redis, True)

        self.assertDictEqual(results[0], expected_result_1)

    def test_get_job_data_all_jobs_two_jobs(self):
        project_name = 'apple'
        data = {
            'project': project_name,
            'user': 'potter',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': self._foundations_serialize([{'harry': 'weasley'}]),
            'metrics': self._fast_serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'tags': {
                'bep': 'bip'
            }
        }
        job_id_1 = 'sushine'
        job_id_2 = 'rain'

        self._sadd_redis_project_name(project_name, job_id_1)
        self._sadd_redis_project_name(project_name, job_id_2)
        self._load_data_new_job(job_id_1, data)
        self._load_data_new_job(job_id_2, data)

        expected_result_1 = {
            'project_name': project_name,
            'job_id': job_id_1,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'harry': 'weasley'}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123'),
            'tags': {
                'bep': 'bip'
            }
        }

        expected_result_2 = {
            'project_name': project_name,
            'job_id': job_id_2,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'harry': 'weasley'}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123'),
            'tags': {
                'bep': 'bip'
            }
        }

        results = JobDataRedis.get_all_jobs_data(
            project_name, self._redis, True)

        six.assertCountEqual(self,
                             results, [expected_result_1, expected_result_2])

    def test_get_job_data_handles_missing_keys(self):
        data = {
            'project': 'banana',
            'user': 'hi',
            'parameters': json.dumps({'harry': 'potter'}),
            'state': 'dead',
            'start_time': '456',
            'completed_time': '123'
        }
        job_id = 'the boy who lived'
        redis_pipe = RedisPipelineWrapper(
            self._redis.pipeline())
        job_data = JobDataRedis(redis_pipe, job_id)
        self._load_data_new_job(job_id, data)

        result = job_data.get_job_data(True)
        redis_pipe.execute()
        expected_result = {
            'project_name': 'banana',
            'job_id': job_id,
            'user': 'hi',
            'job_parameters': {'harry': 'potter'},
            'input_params': [],
            'output_metrics': [],
            'status': 'dead',
            'start_time': float('456'),
            'completed_time': float('123'),
            'tags': {}
        }
        self.assertDictEqual(expected_result, result.get())

    @let
    def fake_timestamp(self):
        self.faker.time()
    
    @let
    def fake_job_1(self):
        return self.faker.uuid4()
    
    @let
    def fake_job_2(self):
        return self.faker.uuid4()
    
    def test_list_all_completed_jobs_lists_completed_jobs(self):
        self._set_redis(self.fake_job_1, 'completed_time', self.fake_timestamp)
        self._set_redis(self.fake_job_2, 'completed_time', self.fake_timestamp)
        expected_result = [self.fake_job_1, self.fake_job_2]
        self.assertEqual(expected_result, JobDataRedis.list_all_completed_jobs(self._redis))
    
    def test_is_job_completed_returns_true_if_job_exists(self):
        self._set_redis(self.fake_job_1, 'completed_time', self.fake_timestamp)
        self.assertTrue(JobDataRedis.is_job_completed(self.fake_job_1, self._redis))
    
    def test_is_job_completed_returns_false_if_job_does_not_exist(self):
        self.assertFalse(JobDataRedis.is_job_completed(self.fake_job_1, self._redis))

    def _foundations_serialize(self, data):
        from foundations_internal.foundations_serializer import serialize
        return serialize(data)

    def _fast_serialize(self, data):
        from foundations_internal.fast_serializer import serialize
        return serialize(data)
