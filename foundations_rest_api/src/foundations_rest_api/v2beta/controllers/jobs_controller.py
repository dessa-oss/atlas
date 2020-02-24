
from foundations_rest_api.utils.api_resource import api_resource


@api_resource("/api/v2beta/projects/<string:project_name>/job_listing")
class JobsController(object):
    def index(self):
        from foundations_rest_api.v2beta.models.project import Project
        from foundations_core_rest_api_components.response import Response
        from foundations_core_rest_api_components.lazy_result import LazyResult

        project_name = self.params.pop("project_name")
        jobs_data_future = Project.find_by(name=project_name).only(
            ["name", "jobs", "output_metric_names", "parameters"]
        )
        jobs_data_future = jobs_data_future.apply_filters(self.params, fields=["jobs"])
        fallback = Response(
            "Jobs", LazyResult(lambda: "This project was not found"), status=404
        )
        return Response("Jobs", jobs_data_future, fallback=fallback)
