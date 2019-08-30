"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource

@api_resource('/api/v1/projects/<string:project_name>/metrics')
class ProductionMetricSetsController(object):

    def index(self):
        from foundations_orbit_rest_api.v1.models.production_metric_set import ProductionMetricSet
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        response_body = ProductionMetricSet.all(project_name=project_name).map(self._sort_alphabetically)
        return Response('Models', response_body)

    def _sort_alphabetically(self, body):
        body.sort(key=lambda entry: entry.title['text'])
        return body