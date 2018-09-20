"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource


@api_resource
class CompletedJobsController(object):

    def index(self):
        from foundations_rest_api.v1.models.project import Project

        return Project.find_by(name=self.params['project_name'])
