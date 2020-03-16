
from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.v1.controllers.job_logs_controller import JobLogsController

JobLogsController = api_resource('/api/v2beta/projects/<string:project_name>/job_listing/<string:job_id>/logs')(JobLogsController)