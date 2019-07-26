"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class SyncableDirectory(object):

    def __init__(self, key, directory_path, local_job_id, remote_job_id):
        from foundations_contrib.archiving import load_archive

        self._key = key
        self._directory_path = directory_path
        self._local_job_id = local_job_id
        self._archive = load_archive('artifact_archive')

    def upload(self):
        from foundations_contrib.archiving.upload_artifacts import list_of_files_to_upload_from_artifact_path

        file_listing = list_of_files_to_upload_from_artifact_path(self._directory_path)
        for file in file_listing:
            self._redis().rpush(f'jobs:{self._local_job_id}:synced_artifacts:{self._key}', file)
            self._archive.append_file(f'synced_directories/{self._key}', file, self._local_job_id)

    def download(self):
        file_listing = self._redis().lrange(f'jobs:{self._local_job_id}:synced_artifacts:{self._key}', 0, -1)
        file_listing = [file.decode() for file in file_listing]
        for file in file_listing:
            self._archive.fetch_file_path_to_target_file_path(
                f'synced_directories/{self._key}', 
                file, 
                self._local_job_id,
                f'{self._directory_path}/{file}'
            )

    def _redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection
