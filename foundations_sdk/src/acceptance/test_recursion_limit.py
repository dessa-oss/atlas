"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations.utils import using_python_2


class TestRecursionLimit(unittest.TestCase):

    def setUp(self):
        from acceptance.cleanup import cleanup
        cleanup()

    @unittest.skipIf(using_python_2(), 'skipping due to running python 2')
    def test_recursion_limit_can_be_overridden(self):
        import foundations
        from foundations.job import Job
        from foundations.global_state import deployment_manager

        @foundations.create_stage
        def callback(data):
            return data+1

        stage = callback(0)
        for _ in range(21):
            stage = callback(stage)

        job = Job(stage)
        config = {'recursion_limit': 10000}
        deployment_manager.deploy(config, 'test_job', job)
