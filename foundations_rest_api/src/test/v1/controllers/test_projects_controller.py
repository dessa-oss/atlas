"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch

from foundations_rest_api.v1.controllers.projects_controller import ProjectsController

class TestProjectsController(unittest.TestCase):

    @patch('foundations_rest_api.v1.models.project.Project.all')
    def test_index_returns_all_projects(self, mock):
        mock.return_value = self._make_response('snowbork drones')

        controller = ProjectsController()

        expected_result = [{'name': 'snowbork drones', 'created_at': None, 'owner': None}]
        self.assertEqual(expected_result, controller.index().as_json())

    @patch('foundations_rest_api.v1.models.project.Project.all')
    def test_index_returns_all_projects_different_projects(self, mock):
        mock.return_value = self._make_response('space2vec')

        controller = ProjectsController()

        expected_result = [{'name': 'space2vec', 'created_at': None, 'owner': None}]
        self.assertEqual(expected_result, controller.index().as_json())

    def _make_response(self, name):
        from foundations_rest_api.response import Response
        from foundations_rest_api.v1.models.project import Project

        def _callback():
            return [Project(name=name)]

        return Response('Project', _callback)
