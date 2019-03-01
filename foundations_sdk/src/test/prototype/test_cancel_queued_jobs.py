"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let_patch_mock, let

from foundations.prototype import cancel_queued_jobs

class TestCancelQueuedJobs(Spec):

    mock_config_manager = let_patch_mock('foundations.global_state.config_manager')

    def test_cancel_no_jobs_if_job_list_is_empty(self):
        cancelled_jobs_with_status = cancel_queued_jobs([])
        self.assertEqual({}, cancelled_jobs_with_status)
    
    def test_cancel_fails_if_jobs_deployed_locally(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment

        self.mock_config_manager.config.return_value = {'deployment_type': LocalShellJobDeployment}
        job_list = self._create_job_list(10)
        expected_job_cancel_status = {job_id: False for job_id in job_list}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs(job_list))

    def _create_job_list(self, max_number_of_jobs):
        from uuid import uuid4
        from random import randint

        job_list = []
        number_of_jobs = randint(1, max_number_of_jobs)
        for _ in range(0, number_of_jobs + 1):
            job_list.append(str(uuid4()))

        return job_list