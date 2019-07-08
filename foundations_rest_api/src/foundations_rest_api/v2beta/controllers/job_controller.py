"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource


@api_resource('/api/v2beta/projects/<string:project_name>/job_listing/<string:job_id>')
class JobController(object):

    def delete(self):
        from foundations_contrib.jobs.kubernetes_job import cancel
        from foundations_rest_api.response import Response
        from foundations_rest_api.lazy_result import LazyResult

        cancel(self.job_id)
        
        return Response('Jobs', LazyResult(lambda: f'Job {self.job_id} successfull cancelled'))