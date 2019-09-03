"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestArchiveJobs(Spec):

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def job_id_to_archive(self):
        return self.faker.uuid4()

    @let
    def invalid_job_id(self):
        return self.faker.uuid4()

    @let
    def stage(self):
        def _stage():
            pass
        return _stage

    @set_up
    def set_up(self):
        from acceptance.cleanup import cleanup
        from foundations import archive_jobs

        cleanup()

        self._run_job(self.job_id)
        self._run_job(self.job_id_to_archive)
        self.archive_jobs_result = archive_jobs([self.job_id_to_archive, self.invalid_job_id])

    def test_only_archives_completed_jobs(self):
        self.assertEqual({self.job_id_to_archive: True, self.invalid_job_id: False}, self.archive_jobs_result)

    def test_removes_archived_jobs_from_completed_jobs(self):
        from foundations import get_metrics_for_all_jobs

        job_metrics = get_metrics_for_all_jobs('run_locally')
        original_job_rows = job_metrics[job_metrics['job_id'] == self.job_id]
        archived_job_rows = job_metrics[job_metrics['job_id'] == self.job_id_to_archive]

        self.assertFalse(original_job_rows.empty)
        self.assertTrue(archived_job_rows.empty)

    def _run_job(self, job_id):
        from foundations_spec.extensions import run_process
        run_process(['python', 'main.py'], 'acceptance/fixtures/run_locally', {'FOUNDATIONS_JOB_ID': job_id})

