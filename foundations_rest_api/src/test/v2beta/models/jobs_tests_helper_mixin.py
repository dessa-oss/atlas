"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class JobsTestsHelperMixin(object):

    def _setup_deployment(self, expected_status):
        from foundations_contrib.global_state import config_manager
        from foundations_contrib.global_state import deployment_manager
        from .mocks.scheduler_backend import MockSchedulerBackend
        from .mocks.deployment import MockDeployment

        deployment_manager._scheduler = None
        self._scheduler_backend_instance = MockSchedulerBackend(
            expected_status, [])

        config_manager['deployment_implementation'] = {
            'deployment_type': MockDeployment(lambda: self._scheduler_backend_instance),
        }

    @staticmethod
    def _cleanup():
        from foundations_contrib.global_state import config_manager

        keys = list(config_manager.config().keys())
        for key in keys:
            del config_manager.config()[key]

    def _make_scheduled_job(self, job_name, start_timestamp, duration_timestamp, user, state):
        from foundations.scheduler_job_information import JobInformation

        job_information = JobInformation(
            job_name, start_timestamp, duration_timestamp, state, user)
        self._scheduler_backend_instance._job_information.append(
            job_information)

    def _make_running_job(self, job_name, start_timestamp, duration_timestamp, user):
        return self._make_scheduled_job(job_name, start_timestamp, duration_timestamp, user, 'RUNNING')

    def _make_queued_job(self, job_name, start_timestamp, duration_timestamp, user):
        return self._make_scheduled_job(job_name, start_timestamp, duration_timestamp, user, 'QUEUED')
