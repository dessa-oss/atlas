"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.global_state import app_manager

class TestProjectListingEndpoint(Spec):
    client = app_manager.app().test_client()
    url = '/api/v1/projects'

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @set_up
    def set_up(self):
        self.redis.flushall()
        self._create_project('hana')
        self._create_project('sam')
        self._create_project('danny')

    def _create_project(self, project_name):
        import time
        from foundations_contrib.global_state import redis_connection

        self.redis.execute_command('ZADD', 'projects', 'NX', time.time(), project_name)

    def _get_from_route(self):
        import json

        response = self.client.get(self.url)
        response_data = response.data.decode()
        return json.loads(response_data)

    def test_get_project_listing(self):
        data = self._get_from_route()
        
        self.assertEqual(3, len(data))
        self._assert_project_in('hana', data)
        self._assert_project_in('sam', data)
        self._assert_project_in('danny', data)

    def _assert_project_in(self, project_name, projects):
        for project in projects:
            if project['name'] == project_name:
                return

        raise AssertionError(f'no project with name \'{project_name}\' exists in {projects}')