"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource


@api_resource('/api/v1/projects/<string:project_name>/job_listing')
class JobsController(object):

    def index(self):
        from foundations_rest_api.v1.models.project import Project
        from foundations_core_rest_api_components.response import Response

        project_name = self.params.pop('project_name')
        jobs_data_future = Project.find_by(name=project_name).only(['name', 'jobs'])
        jobs_data_future = jobs_data_future.apply_filters(self.params, fields=['jobs'])
        return Response('Jobs', jobs_data_future)
