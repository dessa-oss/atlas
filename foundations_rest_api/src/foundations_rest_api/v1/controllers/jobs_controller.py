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
        from foundations_rest_api.response import Response
        from foundations_rest_api.result_filters import result_filters

        jobs_data = Project.find_by(name=self.params['project_name']).only(['name', 'jobs']).filter(result_filters, self.params, fields=['jobs'])
        return Response('Jobs', jobs_data)
