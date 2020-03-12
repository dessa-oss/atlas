
from foundations_spec import *

from foundations_rest_api.global_state import app_manager

class TestProjectsListingEndpoint(Spec):
    client = app_manager.app().test_client()
    url = '/api/v2beta/projects'

    def _str_random_uuid(self):
        import uuid
        return str(uuid.uuid4())

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @set_up
    def set_up(self):
        self.project_name_1 = self._str_random_uuid()
        self.project_name_2 = self._str_random_uuid()
        self.project_name_3 = self._str_random_uuid()

        self._create_project(self.project_name_1)
        self._create_project(self.project_name_2)
        self._create_project(self.project_name_3)

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

        self._assert_project_in(self.project_name_1, data)
        self._assert_project_in(self.project_name_2, data)
        self._assert_project_in(self.project_name_3, data)

    def _assert_project_in(self, project_name, projects):
        for project in projects:
            if project['name'] == project_name:
                return

        raise AssertionError(f'no project with name \'{project_name}\' exists in {projects}')