"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.global_state import app_manager


class TestMonitorJobsEndpoint(Spec):

    client = app_manager.app().test_client()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def job_id(self):
        return f"{self.project_name}-{self.monitor_name}_{self.faker.random_int()}"

    @let
    def job_id_2(self):
        return f"{self.project_name}-{self.monitor_name}_{self.faker.random_int()}"

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection

        return redis_connection

    @let
    def url(self):
        return f"/api/v1/projects/{self.project_name}/monitors/{self.monitor_name}/jobs"

    def _get_from_route(self):
        import json

        response = self.client.get(self.url)
        response_data = response.data.decode()
        return json.loads(response_data)

    def _delete_from_route(self, data):
        import json

        response = self.client.delete(self.url, json=data)
        response_data = response.data.decode()
        return json.loads(response_data)

    @set_up
    def set_up(self):
        self.redis.flushall()

    def _data_to_set(self):
        return [
            {
                "project": "so",
                "job_id": self.job_id,
                "user": "pairing",
                "creation_time": 1571931153.0313132,
                "completed_time": 1571931153.6426458,
                "start_time": 1571931153.0313132,
                "state": "completed",
            },
            {
                "project": "so",
                "job_id": self.job_id_2,
                "user": "pairing",
                "creation_time": 1571931156.550436,
                "start_time": 1571931156.550436,
                "state": "running",
            },
        ]

    def _expected_data(self):
        return [
            {
                "project_name": "so",
                "job_id": self.job_id_2,
                "user": "pairing",
                "job_parameters": {},
                "output_metrics": [],
                "status": "running",
                "creation_time": 1571931156.550436,
                "start_time": 1571931156.550436,
                "completed_time": None,
                "tags": {},
            },
            {
                "project_name": "so",
                "job_id": self.job_id,
                "user": "pairing",
                "job_parameters": {},
                "output_metrics": [],
                "status": "completed",
                "creation_time": 1571931153.0313132,
                "start_time": 1571931153.0313132,
                "completed_time": 1571931153.6426458,
                "tags": {},
            },
        ]

    def test_get_monitor_jobs_gets_all_job_data_from_redis(self):

        for job_listing in self._data_to_set():
            job_id = job_listing.pop("job_id")
            self.redis.sadd(
                f"projects:{self.project_name}:monitors:{self.monitor_name}:jobs",
                job_id,
            )
            for job_key, job_value in job_listing.items():
                self.redis.set(f"jobs:{job_id}:{job_key}", job_value)

        job_data = self._get_from_route()
        expected_data = self._expected_data()

        self.assertEqual(expected_data, job_data)

    def test_delete_monitor_job_removes_data_from_redis(self):
        self.maxDiff = None
        for job_listing in self._data_to_set():
            job_id = job_listing.pop("job_id")
            self.redis.sadd(
                f"projects:{self.project_name}:monitors:{self.monitor_name}:jobs",
                job_id,
            )
            for job_key, job_value in job_listing.items():
                self.redis.set(f"jobs:{job_id}:{job_key}", job_value)

        delete_parameters = {
            "project_name": self.project_name,
            "monitor_name": self.monitor_name,
            "job_id": self.job_id,
        }

        self._delete_from_route(delete_parameters)
        job_data = self._get_from_route()
        expected_data = self._expected_data()
        del expected_data[1]

        self.assertEqual(expected_data, job_data)
