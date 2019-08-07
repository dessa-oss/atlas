"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.job import Job

class TestJob(Spec):

    def test_id_returns_id_from_environment(self):
        job = Job({'JOB_ID': 'whatever'})
        self.assertEqual('whatever', job.id())

    def test_id_returns_job_id_from_environment_different_job_id(self):
        job = Job({'JOB_ID': 'sam job'})
        self.assertEqual('sam job', job.id())

    def test_root_returns_path_to_job_archive_on_disk(self):
        job = Job({'JOB_ID': 'whatever'})
        self.assertEqual('/archive/archive/whatever/artifacts', job.root())

    def test_root_returns_path_to_job_archive_on_disk_different_job_id(self):
        job = Job({'JOB_ID': 'sam_job'})
        self.assertEqual('/archive/archive/sam_job/artifacts', job.root())