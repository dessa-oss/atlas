"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource


@api_resource('/api/v1/login')
class SessionController(object):

    def post(self):
        from foundations_rest_api.v1.models.project import Project
        from foundations_rest_api.response import Response

        project_name = 'buckbuck'
        completed_jobs_future = Project.find_by(name=project_name).only(['name', 'completed_jobs'])
        return Response('CompletedJobs', completed_jobs_future)
