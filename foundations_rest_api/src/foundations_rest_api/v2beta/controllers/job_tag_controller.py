
from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response


@api_resource(
    "/api/v2beta/projects/<string:project_name>/job_listing/<string:job_id>/tags/<string:key>"
)
class JobTagController(object):
    def delete(self):
        from foundations_rest_api.global_state import redis_connection

        job_annotations_key = f"jobs:{self._job_id()}:annotations"
        redis_connection.hdel(job_annotations_key, self._key())

        return Response(
            "Jobs",
            LazyResult(
                lambda: f"Tag key: {self._key()} deleted from job {self._job_id()}"
            ),
        )

    def _job_id(self):
        return self.params["job_id"]

    def _key(self):
        return self.params["key"]
