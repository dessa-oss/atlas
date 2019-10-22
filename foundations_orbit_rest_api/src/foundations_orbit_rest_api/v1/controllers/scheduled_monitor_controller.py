"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource


@api_resource('/api/v1/projects/<string:project_name>/monitors/<string:name>')
class ScheduledMonitorController(object):

    def index(self):
        from foundations_orbit_rest_api.v1.models.scheduled_monitor import ScheduledMonitor
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        monitor_name = self.params.pop('name')

        response = ScheduledMonitor.get(project_name=project_name, name=monitor_name)

        failure_response_data = {
            'project_name': project_name,
            'monitor_name': monitor_name,
            'error': 'does not exist'
        }

        fallback = Response('asdf', LazyResult(lambda: failure_response_data), status=404)

        return Response('ScheduledMonitor', response, status=200, fallback=fallback)

    def delete(self):
        from foundations_orbit_rest_api.v1.models.scheduled_monitor import ScheduledMonitor
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        monitor_name = self.params.pop('name')

        response = ScheduledMonitor.delete(project_name=project_name, name=monitor_name)

        failure_response_data = {
            'project_name': project_name,
            'monitor_name': monitor_name,
            'error': 'does not exist'
        }

        fallback = Response('asdf', LazyResult(lambda: failure_response_data), status=404)

        return Response('ScheduledMonitor', response, status=204, fallback=fallback)

    def patch(self):
        from foundations_orbit_rest_api.v1.models.scheduled_monitor import ScheduledMonitor
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        monitor_name = self.params.pop('name')
        schedule = self.params.pop('schedule')

        fallback = ScheduledMonitorController._get_failure_response(project_name, monitor_name)

        response = ScheduledMonitor.patch(project_name=project_name, name=monitor_name, schedule=schedule)

        return Response('ScheduledMonitor', response, status=204, fallback=fallback)

    @staticmethod
    def _get_failure_response(project_name, monitor_name):
        from foundations_core_rest_api_components.response import Response
        from foundations_core_rest_api_components.lazy_result import LazyResult

        failure_response_data = {
            'project_name': project_name,
            'monitor_name': monitor_name,
            'error': 'does not exist'
        }

        return Response('asdf', LazyResult(lambda: failure_response_data), status=404)




