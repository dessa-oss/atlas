"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

@api_resource('/api/v1/projects')
class ProjectsController(object):
    
    def index(self):
        from foundations_rest_api.v1.models.project import Project
        return Project.all().only(['name'])