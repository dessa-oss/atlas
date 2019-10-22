"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource


@api_resource('/api/v1/projects/<string:project_name>/monitors/<string:monitor_name>')
class ScheduledMonitorController(object):

    def index(self):
        from foundations_orbit_rest_api.v1.models.scheduled_monitor import ScheduledMonitor
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        monitor_name = self.params.pop('monitor_name')

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
        monitor_name = self.params.pop('monitor_name')

        response = ScheduledMonitor.delete(project_name=project_name, name=monitor_name)

        failure_response_data = {
            'project_name': project_name,
            'monitor_name': monitor_name,
            'error': 'does not exist'
        }

        fallback = Response('asdf', LazyResult(lambda: failure_response_data), status=404)

        return Response('ScheduledMonitor', response, status=204, fallback=fallback)

    def put(self):
        from foundations_contrib.cli.orbit_monitor_package_server import pause, resume
        from http import HTTPStatus
        project_name = self.params.pop('project_name')
        monitor_name = self.params.pop('monitor_name')
        env = 'scheduler'

        status = self.params.get('status', None)
        if status == 'resume' or status == 'active':
            resume(project_name, monitor_name, env)
            return self._response(HTTPStatus.NO_CONTENT)
        elif status == 'pause':
            pause(project_name, monitor_name, env)
            return self._response(HTTPStatus.NO_CONTENT)
        else:
            return self._response(HTTPStatus.BAD_REQUEST)

    def _response(self, error, cookie=None):
        from foundations_core_rest_api_components.response import Response
        return Response.constant(error.phrase, status=error.value, cookie=cookie)
