"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.jobs.kubernetes_job import cancel
import foundations_contrib

class TestKubernetesJob(Spec):

    mock_subprocess_run = let_patch_mock('subprocess.run')

    @let
    def job_id(self):
        return self.faker.uuid4()

    def test_cancel_deletes_job(self):
        cancel(self.job_id)
        self.mock_subprocess_run.assert_called_with(['bash', './delete_job.sh', self.job_id], cwd=foundations_contrib.root() / 'resources/jobs')
