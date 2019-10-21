"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 10 2019
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource
from http import HTTPStatus

@api_resource('/api/v1/projects/<string:project_name>/monitors/<string:monitor_name>')
class MonitorController:

    def put(self):
        from foundations_contrib.cli.orbit_monitor_package_server import pause, resume
        project_name = self.params.pop('project_name')
        monitor_name = self.params.pop('monitor_name')
        env = 'scheduler'

        status = self.params.get('status', None)
        if status == 'resume':
            resume(project_name, monitor_name, env)
            return self._response(HTTPStatus.NO_CONTENT)
        elif status == 'pause':
            pause(project_name, monitor_name, env)
            return self._response(HTTPStatus.NO_CONTENT)
        else:
            print('failed to trigger appropriate condition')

    def _response(self, error, cookie=None):
        from foundations_core_rest_api_components.response import Response

        return Response.constant(error.phrase, status=error.value, cookie=cookie)
