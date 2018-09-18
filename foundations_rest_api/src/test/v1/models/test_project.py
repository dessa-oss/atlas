"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.v1.models.project import Project


class TestProject(unittest.TestCase):
    
    def test_new_project_is_response(self):
        from foundations_rest_api.response import Response

        response = Project.new(name='my first project')
        self.assertTrue(isinstance(response, Response))
    
    def test_new_project_is_response_containing_project(self):
        response = Project.new(name='my first project')
        self.assertTrue(isinstance(response.evaluate(), Project))
    
    def test_new_project_has_name(self):
        response = Project.new(name='my first project')
        self.assertEqual('my first project', response.evaluate().name)
    
    def test_new_project_has_name_different_name(self):
        response = Project.new(name='my favourite project')
        self.assertEqual('my favourite project', response.evaluate().name)