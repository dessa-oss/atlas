"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *

class TestEmptyJob(Spec):

    def test_serialize_returns_empty_binary_data(self):
        from foundations_contrib.job_bundling.empty_job import EmptyJob
        self.assertEqual(b'', EmptyJob().serialize())
