"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.projects import set_project_name


class TestProjects(unittest.TestCase):

    def test_set_project_name_sets_project_name(self):
        from foundations.global_state import foundations_context

        set_project_name('some project')
        self.assertEqual(
            'some project', foundations_context.pipeline_context().provenance.project_name)

    def test_set_project_name_sets_project_name_different_name(self):
        from foundations.global_state import foundations_context

        set_project_name('some different project name')
        self.assertEqual('some different project name',
                         foundations_context.pipeline_context().provenance.project_name)

    def test_set_project_name_is_global(self):
        from foundations.global_state import foundations_context
        import foundations

        foundations.set_project_name('some project')
        self.assertEqual(
            'some project', foundations_context.pipeline_context().provenance.project_name)

    def test_set_project_name_is_global(self):
        from foundations.global_state import foundations_context
        import foundations

        foundations.set_project_name('some different project name')
        self.assertEqual('some different project name',
                         foundations_context.pipeline_context().provenance.project_name)
