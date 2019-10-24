"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource

@api_resource('/api/v1/projects/<string:project_name>/monitors/<string:monitor_name>/jobs')
class MonitorJobsController(object):

    def index(self):
        from foundations_orbit_rest_api.v1.models.monitor import Monitor
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        monitor_name = self.params.pop('monitor_name')

        response_body = Monitor.job_ids_from_monitors_dictionary(project_name, monitor_name)

        failure_response_data = {
            'project_name': project_name,
            'monitor_name': monitor_name,
            'error': 'does not exist'
        }

        fallback = Response('asdf', LazyResult(lambda: failure_response_data), status=404)

        return Response('Monitors', response_body, status=200, fallback=fallback)

    def delete(self):
        from foundations_orbit_rest_api.v1.models.monitor import Monitor
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        monitor_name = self.params.pop('monitor_name')
        job_id = self.params.pop('job_id')

        response_body = Monitor.delete_job(project_name, monitor_name, job_id)

        failure_response_data = {
            'project_name': project_name,
            'monitor_name': monitor_name,
            'job_id': job_id,
            'error': 'does not exist'
        }

        fallback = Response('asdf', LazyResult(lambda: failure_response_data), status=404)

        return Response('Monitors', response_body, fallback=fallback)

