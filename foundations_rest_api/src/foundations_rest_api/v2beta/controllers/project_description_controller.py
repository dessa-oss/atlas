"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response

@api_resource('/api/v2beta/projects/<string:project_name>/description')
class ProjectDescriptionController(object):
    
    def show(self):
        return Response('Jobs', LazyResult(self._project_description))

    def update(self):
        from foundations_contrib.global_state import redis_connection
        
        description_key = f'projects:{self.params["project_name"]}:description'
        redis_connection.set(description_key, self.params['project_description'])

    def _project_description(self):
        from foundations_contrib.global_state import redis_connection

        description_key = f'projects:{self.params["project_name"]}:description'
        description = (redis_connection.get(description_key) or b'').decode()
        return {'project_description': description}
