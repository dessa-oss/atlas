"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

from foundations.scheduler_job_information import JobInformation

class LegacyBackend(object):
    """The legacy backend for the Scheduler class, where job information is based off of file metadata.
        Arguments:
            remote_clock: {*Clock} -- Implementation of a class that gets the time on a remote machine.
            bucket_stat_scanner_class: {Class} -- Class name for a class that gets metadata for all files in a directory-like entity.
            jobs_path: {str} -- Path to directory-like entity which contains jobs that are queued to run.
            archive_path: {str} -- Path to directory-like entity which contains jobs that are either running or have finished running.
            results_path: {str} -- Path to directory-like entity which contains results tarballs for jobs that have finished running.
    """

    def __init__(self, remote_clock, bucket_stat_scanner_class, jobs_path, archive_path, results_path):
        self._remote_clock = remote_clock
        self._jobs_path_scanner = bucket_stat_scanner_class(jobs_path)
        self._archive_path_scanner = bucket_stat_scanner_class(archive_path)
        self._results_path_scanner = bucket_stat_scanner_class(results_path)

    def get_paginated(self, start_index, number_to_get, status):
        """Get paginated job information.  Will raise a ValueError if the status on which to filter is not supported.
            Arguments:
                start_index: {int} -- The index at which to start getting jobs.  Ignored for this class.
                number_to_get: {int} -- The number of jobs to return.  Ignored for this class.
                status: {str} -- The status string on which to filter.  'QUEUED', 'RUNNING', and 'COMPLETED' are supported here.  The None value is supported as well - it will get all jobs.

        Returns:
            generator -- An iterable containing the jobs as specified by the arguments.
        """

        if status == "QUEUED":
            return self._get_queued_jobs()
        elif status == "RUNNING":
            return self._get_running_jobs()
        elif status == "COMPLETED":
            return self._get_completed_jobs()
        elif status is None:
            return self._get_all_jobs()

        raise ValueError("Unsupported status: " + status)

    def _get_queued_jobs(self):
        host_time = self._remote_clock.time()

        for dir_entry in self._jobs_path_scanner.scan():
            uuid, user_submitted, submitted_timestamp = LegacyBackend._extract_info(dir_entry)

            yield JobInformation(uuid, submitted_timestamp, host_time - submitted_timestamp, "QUEUED", user_submitted)

    def _get_running_jobs(self):
        filter_function = lambda job_info: (job_info.status() == "RUNNING")
        return filter(filter_function, self._get_running_and_completed_jobs())

    def _get_completed_jobs(self):
        filter_function = lambda job_info: (job_info.status() == "COMPLETED")
        return filter(filter_function, self._get_running_and_completed_jobs())
        
    def _get_running_and_completed_jobs(self):
        done_dict = {dir_entry["filename"]: dir_entry["last_modified"] for dir_entry in self._results_path_scanner.scan()}
        host_time = self._remote_clock.time()

        for dir_entry in self._archive_path_scanner.scan():
            uuid, user_submitted, submitted_timestamp = LegacyBackend._extract_info(dir_entry)

            if dir_entry["filename"] in done_dict:
                end_timestamp = done_dict[dir_entry["filename"]]
                status = "COMPLETED"
            else:
                end_timestamp = host_time
                status = "RUNNING"

            yield JobInformation(uuid, submitted_timestamp, end_timestamp - submitted_timestamp, status, user_submitted)

    def _get_all_jobs(self):
        import itertools
        return itertools.chain(self._get_queued_jobs(), self._get_running_and_completed_jobs())

    @staticmethod
    def _extract_info(dir_entry):
        from os.path import splitext

        uuid, _ = splitext(dir_entry["filename"])
        user_submitted = dir_entry["owner"]
        submitted_timestamp = dir_entry["last_modified"]
        
        return uuid, user_submitted, submitted_timestamp