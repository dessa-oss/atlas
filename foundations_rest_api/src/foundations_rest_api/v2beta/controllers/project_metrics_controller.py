"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response

@api_resource('/api/v2beta/projects/<string:project_name>/overview_metrics')
class ProjectMetricsController(object):

    def index(self):
        return Response('Jobs', LazyResult(self._get_metrics))

    def _get_metrics(self):
        from foundations_contrib.global_state import redis_connection
        from foundations_internal.fast_serializer import deserialize

        project_key = f'projects:{self.project_name}:metrics'
        project_metrics = redis_connection.hgetall(project_key)
        result = []
        # for encoded_key, serialized_value in project_metrics.items():