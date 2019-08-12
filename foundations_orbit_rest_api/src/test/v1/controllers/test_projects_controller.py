"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.controllers.projects_controller import ProjectsController

class TestProjectsController(Spec):

    def test_projects_controller_comes_from_core_rest_api_components_module(self):
        import foundations_core_rest_api_components.v1.controllers.projects_controller as core
        self.assertEqual(core.ProjectsController, ProjectsController)