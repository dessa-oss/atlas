"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

from foundations.scheduler_legacy_backend import LegacyBackend

class LocalBackend(LegacyBackend):
    """The scheduler backend for local shell deployment.  Only supports completed jobs - data fetched from archives configured in yaml.
    """

    def __init__(self):
        pass

    def get_paginated(self, start_index, number_to_get, status):
        """Get paginated job information.  Will raise a ValueError if the status on which to filter is not supported.
            Arguments:
                start_index: {int} -- The index at which to start getting jobs.  Ignored for this class.
                number_to_get: {int} -- The number of jobs to return.  Ignored for this class.
                status: {str} -- The status string on which to filter.  'COMPLETED' is supported here.  The None value is supported as well and is equivalent to 'COMPLETED'.

        Returns:
            generator -- An iterable containing the jobs as specified by the arguments.
        """

        if status == "COMPLETED" or status is None:
            return LocalBackend._get_all_jobs()
        else:
            raise ValueError("Unsupported status: " + status)

    @staticmethod
    def _get_all_jobs():
        from foundations.scheduler_job_information import JobInformation
        from foundations.utils import whoami

        user_name = whoami()

        for job_name, pipeline_context in LocalBackend._get_contexts():
            global_stage_context = pipeline_context.global_stage_context

            start_time = global_stage_context.start_time
            duration = global_stage_context.delta_time

            yield JobInformation(job_name, int(start_time), int(duration), "COMPLETED", user_name)

    @staticmethod
    def _get_contexts():
        from foundations.pipeline_context import PipelineContext
        from foundations.job_persister import JobPersister

        with JobPersister.load_archiver_fetch() as archiver_fetch:
            for archiver in archiver_fetch.fetch_archivers():
                pipeline_context = PipelineContext()
                pipeline_context.load_miscellaneous_from_archive(archiver)

                yield archiver.pipeline_name(), pipeline_context