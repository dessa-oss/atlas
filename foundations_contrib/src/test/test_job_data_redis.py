"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
import json
import fakeredis
from mock import patch
import six

from foundations_contrib.job_data_redis import JobDataRedis
from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
from foundations.global_state import redis_connection


class TestJobDataRedis(unittest.TestCase):

    def setUp(self):
        self._redis = fakeredis.FakeStrictRedis()
        self._redis.flushdb()

    def _set_redis(self, job_id, parameter, data):
        self._redis.set('jobs:{}:{}'.format(job_id, parameter), data)

    def _rpush_redis(self, job_id, parameter, data):
        self._redis.rpush('jobs:{}:{}'.format(job_id, parameter), data)

    def _sadd_redis_input_param(self, project_name, data):
        self._redis.sadd('projects:{}:input_parameter_names'.format(project_name), data)

    def _load_data_new_job(self, job_id, data, project_name):
        set_parameter_name = ['project', 'start_time',
                              'completed_time', 'user', 'state', 'parameters', 'input_parameters']
        rpush_parameter_name = ['metrics']

        for key, value in data.items():
            if key in set_parameter_name:
                self._set_redis(job_id, key, value)
            if key in rpush_parameter_name:
                self._rpush_redis(job_id, key, value)
            if key == 'input_parameter_names':
                self._sadd_redis_input_param(project_name, value)

    def _sadd_redis_project_name(self, project_name, job_id):
        self._redis.sadd(
            'project:{}:jobs:running'.format(project_name), job_id)

    def test_get_job_data_gets_data(self):
        from foundations_internal.fast_serializer import serialize
        project_name = 'banana'
        data = {
            'project': project_name,
            'user': 'potter',
            'parameters': json.dumps({'harry': 'potter'}),
            'input_parameters': json.dumps([{'argument': {'name': 'ron', 'value': 'weasley'}, 'stage_uuid': '978'}]),
            'metrics': serialize(('123', 'hermione', 'granger')),
            'state': 'dead',
            'start_time': '456',
            'completed_time': '123',
            'input_parameter_names': json.dumps({'parameter_name': 'idk','stage_uuid': '978','time': 12314})
        }
        job_id = 'the boy who lived'
        redis_pipe = RedisPipelineWrapper(self._redis.pipeline())
        job_data = JobDataRedis(redis_pipe, job_id, project_name)
        self._load_data_new_job(job_id, data, project_name)

        result = job_data.get_job_data()
        redis_pipe.execute()
        expected_result = {
            'project_name': project_name,
            'job_id': job_id,
            'user': 'potter',
            'job_parameters': {'harry': 'potter'},
            'input_params': [{'argument': {'name': 'ron_0', 'value': 'weasley'}, 'stage_uuid': '978'}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'dead',
            'start_time': float('456'),
            'completed_time': float('123')
        }
        self.assertDictEqual(expected_result, result.get())

    def test_get_job_data_gets_data_different_data(self):
        from foundations_internal.fast_serializer import serialize
        project_name = 'apple'
        job_id = 'sushine'
        stage_uuid = '9898'
        data = {
            'project': project_name,
            'user': 'potter',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': json.dumps([{'argument': {'name': 'harry', 'value': 'weasley'}, 'stage_uuid': stage_uuid}]),
            'metrics': serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'input_parameter_names': json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid,'time': 12314})
        }
        redis_pipe = RedisPipelineWrapper(self._redis.pipeline())
        job_data = JobDataRedis(redis_pipe, job_id, project_name)
        self._load_data_new_job(job_id, data, project_name)

        result = job_data.get_job_data()
        redis_pipe.execute()

        expected_result = {
            'project_name': 'apple',
            'job_id': job_id,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'argument': {'name': 'harry_0', 'value': 'weasley'}, 'stage_uuid': '9898'}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123')
        }

        self.assertDictEqual(expected_result, result.get())

    def test_get_job_data_all_jobs_single_job(self):
        from foundations_internal.fast_serializer import serialize
        project_name = 'apple'
        job_id_1 = 'sushine'
        stage_uuid = 'my_stage'
        data = {
            'project': project_name,
            'user': 'potter',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': json.dumps([{'argument': {'name': 'harry', 'value': 'weasley'}, 'stage_uuid': stage_uuid}]),
            'metrics': serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'input_parameter_names': json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid,'time': 12314})  
        }
        

        self._sadd_redis_project_name(project_name, job_id_1)
        self._load_data_new_job(job_id_1, data, project_name)

        expected_result_1 = {
            'project_name': project_name,
            'job_id': job_id_1,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'argument': {'name': 'harry_0', 'value': 'weasley'}, 'stage_uuid': stage_uuid}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123')
        }

        results = JobDataRedis.get_all_jobs_data(project_name, self._redis)

        self.assertDictEqual(results[0], expected_result_1)

    def test_get_job_data_all_jobs_single_job_different_data(self):
        from foundations_internal.fast_serializer import serialize
        project_name = 'pomme'
        job_id_1 = 'sushine'
        stage_uuid = 'best_stage'
        data = {
            'project': project_name,
            'user': 'baker',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': json.dumps([{'argument': {'name': 'harry', 'value': 'bigfoot'}, 'stage_uuid': stage_uuid}]),
            'metrics': serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'input_parameter_names': json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid,'time': 12314})          
        }

        self._sadd_redis_project_name(project_name, job_id_1)
        self._load_data_new_job(job_id_1, data, project_name)

        expected_result_1 = {
            'project_name': project_name,
            'job_id': job_id_1,
            'user': 'baker',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'argument': {'name': 'harry_0', 'value': 'bigfoot'}, 'stage_uuid': stage_uuid}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123')
        }

        results = JobDataRedis.get_all_jobs_data(
            project_name, self._redis)

        self.assertDictEqual(results[0], expected_result_1)

    def test_get_job_data_all_jobs_two_jobs(self):
        from foundations_internal.fast_serializer import serialize
        project_name = 'apple'
        job_id_1 = 'sushine'
        job_id_2 = 'rain'
        stage_uuid = 'favourite_stage'

        data = {
            'project': project_name,
            'user': 'potter',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': json.dumps([{'argument': {'name': 'harry', 'value': 'bigfoot'}, 'stage_uuid': stage_uuid}]),
            'metrics': serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'input_parameter_names': json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid,'time': 12314})                
        }

        self._sadd_redis_project_name(project_name, job_id_1)
        self._sadd_redis_project_name(project_name, job_id_2)
        self._load_data_new_job(job_id_1, data, project_name)
        self._load_data_new_job(job_id_2, data, project_name)

        expected_result_1 = {
            'project_name': project_name,
            'job_id': job_id_1,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'argument': {'name': 'harry_0', 'value': 'bigfoot'}, 'stage_uuid': stage_uuid}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123'),
            
        }

        expected_result_2 = {
            'project_name': project_name,
            'job_id': job_id_2,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'argument': {'name': 'harry_0', 'value': 'bigfoot'}, 'stage_uuid': stage_uuid}],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123')
        }

        results = JobDataRedis.get_all_jobs_data(
            project_name, self._redis)

        six.assertCountEqual(self,
                             results, [expected_result_1, expected_result_2])

    def test_get_job_data_handles_missing_keys(self):
        from foundations_internal.fast_serializer import serialize
        project_name = 'banana'
        data = {
            'project': project_name ,
            'user': 'hi',
            'parameters': json.dumps({'harry': 'potter'}),
            'state': 'dead',
            'start_time': '456',
            'completed_time': '123'
        }
        job_id = 'the boy who lived'
        redis_pipe = RedisPipelineWrapper(
            self._redis.pipeline())
        job_data = JobDataRedis(redis_pipe, job_id, project_name)
        self._load_data_new_job(job_id, data, project_name)

        result = job_data.get_job_data()
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
            'completed_time': float('123')
        }
        self.assertDictEqual(expected_result, result.get())

    def test_get_job_with_multiple_stages(self):
        from foundations_internal.fast_serializer import serialize
        project_name = 'apple'
        job_id_1 = 'sushine'
        stage_uuid_1 = 'my_stage'
        stage_uuid_2 = 'the best stage'
        stage_uuid_3 = 'even better'
        data = {
            'project': project_name,
            'user': 'potter',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': json.dumps([{'argument': {'name': 'harry', 'value': 'weasley'}, 'stage_uuid': stage_uuid_1},
                                        {'argument': {'name': 'harry', 'value': 'weasley'}, 'stage_uuid': stage_uuid_2},
                                        {'argument': {'name': 'harry', 'value': 'ginny'}, 'stage_uuid': stage_uuid_3}
                                        ]),
            'metrics': serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'input_parameter_names': json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid_1,'time': 12314})  
        }
        

        self._sadd_redis_project_name(project_name, job_id_1)
        self._load_data_new_job(job_id_1, data, project_name)
    
        self._sadd_redis_input_param(project_name, json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid_2,'time': 12500}))
        self._sadd_redis_input_param(project_name, json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid_3,'time': 12800}))

        expected_result = {
            'project_name': project_name,
            'job_id': job_id_1,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'argument': {'name': 'harry_0', 'value': 'weasley'}, 'stage_uuid': stage_uuid_1},
                            {'argument': {'name': 'harry_1', 'value': 'weasley'}, 'stage_uuid': stage_uuid_2},
                            {'argument': {'name': 'harry_2', 'value': 'ginny'}, 'stage_uuid': stage_uuid_3}
                            ],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123')
        }

        results = JobDataRedis.get_all_jobs_data(project_name, self._redis)

        self.assertDictEqual(results[0], expected_result)
    
    def test_get_job_multiple_stages_multiple_jobs(self):
        from foundations_internal.fast_serializer import serialize
        project_name = 'apple'
        job_id_1 = 'sushine'
        job_id_2 = 'rain'
        stage_uuid_1 = 'my_stage'
        stage_uuid_2 = 'the best stage'
        stage_uuid_3 = 'even better'

        data = {
            'project': project_name,
            'user': 'potter',
            'parameters': json.dumps({'ron': 'potter'}),
            'input_parameters': json.dumps([{'argument': {'name': 'harry', 'value': 'weasley'}, 'stage_uuid': stage_uuid_1},
                                        {'argument': {'name': 'harry', 'value': 'weasley'}, 'stage_uuid': stage_uuid_2},
                                        {'argument': {'name': 'harry', 'value': 'ginny'}, 'stage_uuid': stage_uuid_3}
                                        ]),
            'metrics': serialize(('123', 'hermione', 'granger')),
            'state': 'completed',
            'start_time': '1231003123',
            'completed_time': '123',
            'input_parameter_names': json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid_1,'time': 12314})  
        }

        self._sadd_redis_project_name(project_name, job_id_1)
        self._sadd_redis_project_name(project_name, job_id_2)
        self._load_data_new_job(job_id_1, data, project_name)
        self._load_data_new_job(job_id_2, data, project_name)
    
            
        self._sadd_redis_input_param(project_name, json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid_2,'time': 12500}))
        self._sadd_redis_input_param(project_name, json.dumps({'parameter_name': 'dun','stage_uuid': stage_uuid_3,'time': 12800}))

        expected_result_1 = {
            'project_name': project_name,
            'job_id': job_id_1,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'argument': {'name': 'harry_0', 'value': 'weasley'}, 'stage_uuid': stage_uuid_1},
                            {'argument': {'name': 'harry_1', 'value': 'weasley'}, 'stage_uuid': stage_uuid_2},
                            {'argument': {'name': 'harry_2', 'value': 'ginny'}, 'stage_uuid': stage_uuid_3}
                            ],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123')
        }
        expected_result_2 = {
            'project_name': project_name,
            'job_id': job_id_2,
            'user': 'potter',
            'job_parameters': {'ron': 'potter'},
            'input_params': [{'argument': {'name': 'harry_0', 'value': 'weasley'}, 'stage_uuid': stage_uuid_1},
                            {'argument': {'name': 'harry_1', 'value': 'weasley'}, 'stage_uuid': stage_uuid_2},
                            {'argument': {'name': 'harry_2', 'value': 'ginny'}, 'stage_uuid': stage_uuid_3}
                            ],
            'output_metrics': [('123', 'hermione', 'granger')],
            'status': 'completed',
            'start_time': float('1231003123'),
            'completed_time': float('123')
        }
        results = JobDataRedis.get_all_jobs_data(
            project_name, self._redis)

        six.assertCountEqual(self,
                             results, [expected_result_1, expected_result_2])