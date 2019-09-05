"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

class TestProjectController(Spec):

    mock_set_default_model = let_patch_mock('foundations_orbit_rest_api.v1.models.project.Project.set_default_model')

    @let
    def project_controller(self):
        from foundations_orbit_rest_api.v1.controllers.project_controller import ProjectController
        return ProjectController()
    
    def test_project_put_request_calls_set_default_model_with_correct_model_name(self):
        self._set_params_and_put()
        self.mock_set_default_model.assert_called_with('test_project', 'model')

    def test_project_put_request_returns_status_code_200_if_successful(self):
        self.mock_set_default_model.return_value = True
        response = self._set_params_and_put()
        self.assertEqual(200, response.status())

    def test_project_put_request_returns_status_code_417_if_failed(self):
        self.mock_set_default_model.return_value = False
        response = self._set_params_and_put()
        self.assertEqual(417, response.status())

    def _set_params_and_put(self):
        self.project_controller.params = {'default_model': 'model', 'project_name': 'test_project'}
        return self.project_controller.put()

