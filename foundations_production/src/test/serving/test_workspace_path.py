"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving import workspace_path

class TestWorkspacePath(Spec):

    @let
    def job_id(self):
        return self.faker.uuid4()
    
    def test_workspace_path_constructs_workspace_path_from_job_id(self):
        expected_path = '/tmp/foundations_workspaces/{}'.format(self.job_id)
        self.assertEqual(expected_path, workspace_path(self.job_id))