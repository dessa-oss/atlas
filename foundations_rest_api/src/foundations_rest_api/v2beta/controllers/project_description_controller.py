
from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response

@api_resource('/api/v2beta/projects/<string:project_name>/description')
class ProjectDescriptionController(object):
    
    def show(self):
        return Response('ProjectDescription', LazyResult(self._project_description))

    def update(self):
        return Response('ProjectDescription', LazyResult(self._update_project_description))

    def _update_project_description(self):
        description_key = self._project_description_key()
        self._redis().set(description_key, self.params['project_description'])
        return f'Updated description for {self.params["project_name"]}'

    def _redis(self):
        from foundations_rest_api.global_state import redis_connection
        return redis_connection

    def _project_description(self):
        description_key = self._project_description_key()
        description = (self._redis().get(description_key) or b'').decode()
        return {'project_description': description}

    def _project_description_key(self):
        return f'projects:{self.params["project_name"]}:description'
