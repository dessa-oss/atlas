"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let_patch_mock, let

from foundations.prototype import cancel_queued_jobs

class TestCancelQueuedJobs(Spec):
    def test_cancel_no_jobs_if_job_list_is_empty(self):
        cancelled_jobs_with_status = cancel_queued_jobs([])
        self.assertEqual({}, cancelled_jobs_with_status)