"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource


@api_resource('/api/v1/projects/<string:project_name>/monitors/<string:monitor_name>')
class ScheduledMonitorController(object):

    project_name = None
    monitor_name = None

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

    def patch(self):
        from foundations_orbit_rest_api.v1.models.scheduled_monitor import ScheduledMonitor
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        monitor_name = self.params.pop('monitor_name')
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

    def put(self):
        from foundations_contrib.cli.orbit_monitor_package_server import pause, resume
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from http import HTTPStatus

        self.project_name = self.params.pop('project_name')
        self.monitor_name = self.params.pop('monitor_name')
        env = 'scheduler'

        status = self.params.get('status', None)
        if status == 'resume' or status == 'active':
            response = LazyResult(lambda: resume(self.project_name, self.monitor_name, env))
            return self._response(response, status=204, failure_response_msg='failed to resume monitor')
        elif status == 'pause':
            response = LazyResult(lambda: pause(self.project_name, self.monitor_name, env))
            return self._response(response, status=204, failure_response_msg='failed to pause monitor')
        else:
            return self._only_status_code_response(HTTPStatus.BAD_REQUEST)

    def _response(self, response, status=200, failure_response_msg=None, cookie=None):
        from foundations_core_rest_api_components.response import Response
        from foundations_core_rest_api_components.lazy_result import LazyResult

        if failure_response_msg:
            failure_response_data = {
                'project_name': self.project_name,
                'monitor_name': self.monitor_name,
                'error': failure_response_msg
            }
            failure_fallback = Response('ScheduledMonitor', LazyResult(lambda: failure_response_data), status=404)
        else:
            failure_fallback = None

        return Response('ScheduledMonitor', response, status=status, fallback=failure_fallback, cookie=cookie)

    def _only_status_code_response(self, http_status, cookie=None):
        from foundations_core_rest_api_components.response import Response
        return Response.constant(http_status.phrase, status=http_status.value, cookie=cookie)