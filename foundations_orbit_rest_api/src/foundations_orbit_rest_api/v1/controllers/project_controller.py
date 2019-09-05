"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource
from http import HTTPStatus

@api_resource('/api/v1/projects/<string:project_name>')
class ProjectController(object):
    
    def put(self):
        return self._set_default_model(self._default_model)

    def _set_default_model(self, model):
        from foundations_orbit_rest_api.v1.models.project import Project

        project_name = self.params.pop('project_name')
        success = Project.set_default_model(project_name, model)

        if success:
            return self._response(HTTPStatus.OK)
        return self._response(HTTPStatus.EXPECTATION_FAILED)

    def _response(self, error, cookie=None):
        from foundations_core_rest_api_components.response import Response
    
        return Response.constant(error.phrase, status=error.value, cookie=cookie)

    @property
    def _default_model(self):
        return self.params.get('default_model')