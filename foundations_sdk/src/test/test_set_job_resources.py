"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import foundations

class TestSetJobResources(Spec):

    def test_set_job_resources_is_available_in_sdk(self):
        from foundations_contrib.set_job_resources import set_job_resources
        self.assertIs(set_job_resources, foundations.set_job_resources)

