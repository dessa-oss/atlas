
from foundations_core_rest_api_components.utils.api_resource import api_resource
from foundations_core_rest_api_components.v1.controllers.projects_controller import ProjectsController

ProjectsController = api_resource('/api/v1/projects')(ProjectsController)
