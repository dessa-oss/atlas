"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource

@api_resource('/api/v1/projects/<string:project_name>/model_listing')
class ModelsController(object):

    def index(self):
        from functools import partial

        from foundations_orbit_rest_api.v1.models.model import Model
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        response_body_callback = partial(self._response_body, project_name)
        response_body = Model.all(project_name=project_name).map(response_body_callback)
        return Response('Models', response_body)

    def _response_body(self, project_name, models):
        return {'name': project_name, 'models': models}