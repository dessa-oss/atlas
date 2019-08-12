"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_core_rest_api_components.v1.controllers.projects_controller import ProjectsController
from foundations_core_rest_api_components.utils.api_resource import api_resource

ProjectsController = api_resource('/api/v1/projects')(ProjectsController)
