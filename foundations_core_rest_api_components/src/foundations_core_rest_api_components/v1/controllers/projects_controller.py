
class ProjectsController(object):
    
    def index(self):
        from foundations_core_rest_api_components.v1.models.project import Project
        from foundations_core_rest_api_components.response import Response

        projects_future = Project.all().only(['name', 'created_at', 'owner'])
        return Response('Projects', projects_future)
