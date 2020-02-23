
from foundations_core_rest_api_components.utils.api_resource import api_resource

@api_resource('/api/v1/projects/<string:project_name>/validation_report_list')
class ValidationReportListingsController(object):
    
    def index(self):
        from foundations_core_rest_api_components.response import Response
        from foundations_orbit_rest_api.v1.models.validation_report_listing import ValidationReportListing

        project_name = self.params.pop('project_name')
        return Response('ValidationReportListings', ValidationReportListing.all(project_name=project_name))
