"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_contrib.models.project_listing import ProjectListing

class TestProjectListing(unittest.TestCase):
    
    def setUp(self):
        self._projects = []
        self._redis_connection = Mock()
        self._redis_connection.zrange.side_effect = self._list_projects

    def test_list_projects_lists_empty_projects(self):
        result = ProjectListing.list_projects(self._redis_connection)
        self.assertEqual([], result)

    def test_list_projects_lists_single_project(self):
        self._projects = [(b'my first project', 99343.33)]
        result = ProjectListing.list_projects(self._redis_connection)
        self.assertEqual([{'name': 'my first project', 'created_at': 99343.33}], result)

    def test_list_projects_lists_multiple_projects(self):
        self._projects = [(b'cat and mouse', 3733.33), (b'dog and bear', 4333.23)]
        expected_result = [
            {'name': 'cat and mouse', 'created_at': 3733.33},
            {'name': 'dog and bear', 'created_at': 4333.23},
        ]
        result = ProjectListing.list_projects(self._redis_connection)
        self.assertEqual(expected_result, result)

    def _list_projects(self, key, start, end, withscores):
        if key == 'projects' and start == 0 and end == -1 and withscores:
            return self._projects
        else:
            return []