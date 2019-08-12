"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestProjectsController(Spec):

    def test_projects_controller_comes_from_core_rest_api_components_module(self):
        import foundations_orbit_rest_api.v1.controllers.projects_controller as orbit
        import foundations_core_rest_api_components.v1.controllers.projects_controller as core
        self.assertEqual(core.ProjectsController, orbit.ProjectsController)

    def test_projects_controller_registered_as_api_resource(self):
        import importlib
        import foundations_core_rest_api_components.v1.controllers.projects_controller as core
        import foundations_orbit_rest_api.v1.controllers.projects_controller as orbit

        mock_api_resource = self.patch('foundations_core_rest_api_components.utils.api_resource.api_resource', ConditionalReturn())
        class_decorator = ConditionalReturn()
        decorated_class = Mock()

        mock_api_resource.return_when(class_decorator, '/api/v1/projects')
        class_decorator.return_when(decorated_class, core.ProjectsController)

        importlib.reload(orbit)

        self.assertEqual(decorated_class, orbit.ProjectsController)
